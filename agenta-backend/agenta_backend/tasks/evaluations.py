import asyncio
import logging
import os
import traceback
from collections import defaultdict
from typing import Dict, List

from agenta_backend.models.api.evaluation_model import AppOutput, NewEvaluation
from agenta_backend.models.db_engine import DBEngine
from agenta_backend.models.db_models import (
    AggregatedResult,
    AppDB,
    EvaluationScenarioInputDB,
    EvaluationScenarioOutputDB,
    EvaluationScenarioResult,
    Result,
)
from agenta_backend.services import evaluators_service, llm_apps_service
from agenta_backend.services.db_manager import (
    create_new_evaluation_scenario,
    fetch_app_by_id,
    fetch_app_variant_by_id,
    fetch_evaluation_by_id,
    fetch_evaluator_config,
    fetch_evaluator_config_by_appId,
    fetch_testset_by_id,
    get_deployment_by_objectid,
    update_evaluation,
    update_evaluation_with_aggregated_results,
)
from celery import shared_task, states

# Set logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@shared_task(queue="agenta_backend.tasks.evaluations.evaluate", bind=True)
def evaluate(
    self,
    app_id: str,
    variant_id: str,
    evaluators_config_ids: List[str],
    testset_id: str,
    evaluation_id: str,
    rate_limit_config: Dict[str, int],
):
    """
    Evaluate function that performs the evaluation of an app variant using the provided evaluators and testset.
    Saves the results in the Database

    Args:
        app_id (str): The ID of the app.
        variant_id (str): The ID of the app variant.
        evaluators_config_ids (List[str]): The IDs of the evaluators configurations to be used.
        testset_id (str): The ID of the testset.
        rate_limit_config (Dict[str,int]): See LLMRunRateLimit

    Returns:
        None
    """

    loop = asyncio.get_event_loop()

    try:
        # 1. Fetch data from the database
        loop.run_until_complete(DBEngine().init_db())
        app = loop.run_until_complete(fetch_app_by_id(app_id))
        app_variant_db = loop.run_until_complete(fetch_app_variant_by_id(variant_id))
        app_variant_parameters = app_variant_db.config.parameters
        testset_db = loop.run_until_complete(fetch_testset_by_id(testset_id))
        new_evaluation_db = loop.run_until_complete(
            fetch_evaluation_by_id(evaluation_id)
        )
        evaluator_config_dbs = []
        for evaluator_config_id in evaluators_config_ids:
            evaluator_config = loop.run_until_complete(
                fetch_evaluator_config(evaluator_config_id)
            )
            evaluator_config_dbs.append(evaluator_config)
        deployment_db = loop.run_until_complete(
            get_deployment_by_objectid(app_variant_db.base.deployment)
        )
        uri = _get_deployment_uri(deployment_db)
        # 2. Initialize vars
        evaluators_aggregated_data = {
            evaluator_config_db.id: {
                "evaluator_key": evaluator_config.evaluator_key,
                "results": [],
            }
            for evaluator_config_db in evaluator_config_dbs
        }
        # 3. Invoke the app
        app_outputs: List[AppOutput] = loop.run_until_complete(
            llm_apps_service.batch_invoke(
                uri,
                testset_db.csvdata,
                app_variant_parameters,
                rate_limit_config,
            )
        )

        openapi_parameters = loop.run_until_complete(
            llm_apps_service.get_parameters_from_openapi(uri + "/openapi.json")
        )
        # 4. Evaluate the app ourputss

        if len(testset_db.csvdata) != len(app_outputs):
            loop.run_until_complete(
                update_evaluation(evaluation_id, {"status": "EVALUATION_FAILED"})
            )
            self.update_state(state=states.FAILURE)

            raise ValueError("Length of csv data and app_outputs are not the same")
            return
        for data_point, app_output in zip(testset_db.csvdata, app_outputs):
            # 2. We prepare the inputs
            logger.debug(f"Preparing inputs for data point: {data_point}")
            list_inputs = get_app_inputs(app_variant_parameters, openapi_parameters)
            logger.debug(f"List of inputs: {list_inputs}")
            inputs = [
                EvaluationScenarioInputDB(
                    name=input_item["name"],
                    type="text",
                    value=data_point[
                        input_item["name"]
                        if input_item["type"] != "messages"
                        else "chat"
                    ],  # TODO: We need to remove the hardcoding of chat as name for chat inputs from the FE
                )
                for input_item in list_inputs
            ]
            logger.debug(f"Inputs: {inputs}")
            # 3. We evaluate
            evaluators_results: [EvaluationScenarioResult] = []
            for evaluator_config_db in evaluator_config_dbs:
                logger.debug(f"Evaluating with evaluator: {evaluator_config_db}")
                result = evaluators_service.evaluate(
                    evaluator_key=evaluator_config_db.evaluator_key,
                    output=app_output.output,
                    correct_answer=data_point["correct_answer"],
                    settings_values=evaluator_config_db.settings_values,
                    app_params=app_variant_parameters,
                    inputs=data_point,
                )

                result_object = EvaluationScenarioResult(
                    evaluator_config=evaluator_config_db.id,
                    result=result,
                )
                logger.debug(f"Result: {result_object}")
                evaluators_results.append(result_object)

            # 4. We save the result of the eval scenario in the db
            loop.run_until_complete(
                create_new_evaluation_scenario(
                    user=app.user,
                    organization=app.organization,
                    evaluation=new_evaluation_db,
                    variant_id=variant_id,
                    evaluators_configs=new_evaluation_db.evaluators_configs,
                    inputs=inputs,
                    is_pinned=False,
                    note="",
                    correct_answer=data_point["correct_answer"],
                    outputs=[
                        EvaluationScenarioOutputDB(type="text", value=app_output.output)
                    ],
                    results=evaluators_results,
                )
            )

    except Exception as e:
        logger.error(f"An error occurred during evaluation: {e}")
        traceback.print_exc()
        loop.run_until_complete(
            update_evaluation(evaluation_id, {"status": "EVALUATION_FAILED"})
        )
        self.update_state(state=states.FAILURE)

        return

    aggregated_results = loop.run_until_complete(
        aggregate_evaluator_results(app, evaluators_aggregated_data)
    )
    loop.run_until_complete(
        update_evaluation_with_aggregated_results(
            new_evaluation_db.id, aggregated_results
        )
    )


async def aggregate_evaluator_results(
    app: AppDB, evaluators_aggregated_data: dict
) -> List[AggregatedResult]:
    aggregated_results = []
    for config_id, val in evaluators_aggregated_data.items():
        evaluator_key = val["evaluator_key"] or ""
        results = val["results"] or []
        if evaluator_key != "auto_ai_critique":
            average_value = (
                sum([result.value for result in results]) / len(results)
                if results
                else 0
            )
        elif evaluator_key == "auto_ai_critique":
            try:
                average_value = (
                    sum(
                        [
                            int(result.value)
                            for result in results
                            if isinstance(int(result.value), int)
                        ]
                    )
                    / len(results)
                    if results
                    else 0
                )
            except TypeError:
                average_value = None
        evaluator_config = await fetch_evaluator_config(config_id)
        aggregated_result = AggregatedResult(
            evaluator_config=evaluator_config.id,
            result=Result(type="number", value=average_value),
        )
        aggregated_results.append(aggregated_result)
    return aggregated_results


def _get_deployment_uri(deployment_db) -> str:
    #!NOTE: do not remove! this will be used in github workflow!
    backend_environment = os.environ.get(
        "ENVIRONMENT"
    )  # TODO @abram rename the environment variable to something other than environment!!!
    if backend_environment is not None and backend_environment == "github":
        return f"http://{deployment_db.container_name}"  # TODO: @abram Remove this from here. Move it to the deployment manager
    else:
        return deployment_db.uri.replace(
            "http://localhost", "http://host.docker.internal"
        )


def get_app_inputs(app_variant_parameters, openapi_parameters) -> List[Dict[str, str]]:
    """
    Get a list of application inputs based on the app variant parameters and openapi parameters.

    Args:
        app_variant_parameters (dict): A dictionary containing the app variant parameters.
        openapi_parameters (list): A list of openapi parameters.

    Returns:
        list: A list of dictionaries representing the application inputs, where each dictionary contains the input name and type.
    """
    list_inputs = []
    for param in openapi_parameters:
        if param["type"] == "input":
            list_inputs.append({"name": param["name"], "type": "input"})
        elif param["type"] == "dict":
            for input_name in app_variant_parameters[param["name"]]:
                list_inputs.append({"name": input_name["name"], "type": "dict_input"})
        elif param["type"] == "messages":
            list_inputs.append({"name": param["name"], "type": "messages"})
        elif param["type"] == "file_url":
            list_inputs.append({"name": param["name"], "type": "file_url"})
    return list_inputs
