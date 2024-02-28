import logging
from typing import List
from datetime import datetime

from fastapi import HTTPException

from agenta_backend.models.api.api_models import PaginationParam, SorterParams
from agenta_backend.models.api.observability_models import (
    Span,
    SpanDetail,
    CreateSpan,
    ObservabilityDashboardData,
    Feedback,
    CreateFeedback,
    UpdateFeedback,
    Trace,
    CreateTrace,
    UpdateTrace,
    ObservabilityData,
    GenerationFilterParams,
    ObservabilityDashboardDataRequestParams,
)
from agenta_backend.models.converters import (
    spans_to_pydantic,
    feedback_db_to_pydantic,
    trace_db_to_pydantic,
    get_paginated_data,
)
from agenta_backend.services import db_manager
from agenta_backend.models.db_models import (
    TraceDB,
    SpanStatus,
    Feedback as FeedbackDB,
    SpanDB,
)

from beanie import PydanticObjectId as ObjectId


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


async def get_variant_traces(
    app_id: str, variant_id: str, user_uid: str
) -> List[Trace]:
    """Get the traces for a given app variant.

    Args:
        app_id (str): the app id of the trace
        variant_id (str): the id of the variant

    Returns:
        List[Trace]: the list of traces for the given app variant
    """

    user = await db_manager.get_user(user_uid)
    traces = await TraceDB.find(
        TraceDB.user.id == user.id,
        TraceDB.app_id == app_id,
        TraceDB.variant_id == variant_id,
        fetch_links=True,
    ).to_list()
    return [trace_db_to_pydantic(trace) for trace in traces]


async def create_app_trace(payload: CreateTrace, user_uid: str) -> str:
    """Create a new trace.

    Args:
        payload (CreateTrace): the required payload

    Returns:
        Trace: the created trace
    """

    user = await db_manager.get_user(user_uid)

    # Ensure spans exists in the db
    for span in payload.spans:
        span_db = await SpanDB.find_one(SpanDB.id == ObjectId(span), fetch_links=True)
        if span_db is None:
            raise HTTPException(404, detail=f"Span {span} does not exist")

    trace_db = TraceDB(**payload.dict(), user=user)
    await trace_db.create()
    return str(trace_db.id)


async def get_trace_single(trace_id: str, user_uid: str) -> Trace:
    """Get a single trace.

    Args:
        trace_id (str): the Id of the trace

    Returns:
        Trace: the trace
    """

    user = await db_manager.get_user(user_uid)

    # Get trace
    trace = await TraceDB.find_one(
        TraceDB.id == ObjectId(trace_id), TraceDB.user.id == user.id, fetch_links=True
    )
    return trace_db_to_pydantic(trace)


async def trace_update(trace_id: str, payload: UpdateTrace, user_uid: str) -> bool:
    """Update status of trace.

    Args:
        trace_id (str): the Id of the trace
        payload (UpdateTrace): the required payload

    Returns:
        bool: True if successful
    """

    user = await db_manager.get_user(user_uid)

    # Get trace
    trace = await TraceDB.find_one(
        TraceDB.id == ObjectId(trace_id), TraceDB.user.id == user.id
    )

    await trace.update({"$set": payload.dict(exclude_none=True)})
    return True


async def create_trace_span(payload: CreateSpan) -> str:
    """Create a new span for a given trace.

    Args:
        payload (CreateSpan): the required payload

    Returns:
        str: the created span id
    """

    end_time = datetime.now()
    duration = end_time - payload.start_time
    trace = await TraceDB.find_one(TraceDB.id == ObjectId(payload.trace_id))
    span_db = SpanDB(
        **payload.dict(exclude={"end_time", "duration", "trace_id"}),
        trace=trace,
        end_time=end_time,
        duration=duration.total_seconds(),
    )
    await span_db.create()
    return str(span_db.id)


async def fetch_generation_spans(
    user_uid: str,
    app_id: str,
    pagination: PaginationParam,
    filters: GenerationFilterParams,
    sorters: SorterParams,
) -> List[Span]:
    """Get the spans for a given trace.

    Args:
        user_uid (str): the uid of the user
        trace_type (str): the type of the trace

    Returns:
        List[Span]: the list of spans for the given user
    """

    user = await db_manager.get_user(user_uid)
    spans_db = await SpanDB.find(
        SpanDB.trace.user.id == str(user.id), SpanDB.trace.app_id == app_id
    ).to_list()

    def filter_span(span: Span):
        if filters:
            if filters.variant and span.variant.variant_name != filters.variant:
                return False
            if filters.environment and span.environment != filters.environment:
                return False
        return True

    # Get trace spans
    spans = await spans_to_pydantic(spans_db)
    filtered_generations = filter(filter_span, spans)

    # Sorting logic
    reverse = False
    sort_keys = list(sorters.dict(exclude=None).keys())
    if "created_at" in sort_keys:
        reverse = sorters.created_at == "desc" if sorters else False

    sorted_generations = sorted(
        filtered_generations, key=lambda x: x["created_at"], reverse=reverse
    )
    return get_paginated_data(sorted_generations, pagination)


async def fetch_generation_span_detail(span_id: str, user_uid: str) -> SpanDetail:
    """Get a generation span detail.

    Args:
        span_id (str): The ID of a span
        user_uid (str): The user ID

    Returns:
        SpanDetail: span detail pydantic model
    """

    user = await db_manager.get_user(user_uid)
    span_db = await SpanDB.find_one(
        SpanDB.id == ObjectId(span_id), SpanDB.trace.user.id == user.id
    )
    app_variant_db = await db_manager.fetch_app_variant_by_base_id_and_config_name(
        span_db.trace.base_id, span_db.trace.config_name
    )

    def convert_variables(span_db: SpanDB):
        """
        Converts a list of variables to a list of dictionaries with name and type information.

        Args:
            span_db: A dictionary containing a list of variables under the "inputs" key.

        Returns:
            A list of dictionaries, where each dictionary has the following keys:
                name: The name of the variable.
                type: The type of the variable (string, number, or boolean).
        """

        variables = []
        for variable in span_db.inputs:
            if isinstance(variable, str):
                variable_type = "string"
            elif isinstance(variable, (int, float)):
                variable_type = "number"
            elif isinstance(variable, bool):
                variable_type = "boolean"
            else:
                raise ValueError(f"Unsupported variable type: {type(variable)}")

            variables.append({"name": variable, "type": variable_type})
        return variables

    return SpanDetail(
        **{
            "id": str(span_db.id),
            "created_at": span_db.created_at.isoformat(),
            "variant": {
                "variant_id": str(app_variant_db.id),
                "variant_name": app_variant_db.variant_name,
                "revision": app_variant_db.revision,
            },
            "environment": "",
            "status": {
                "value": span_db.status.value,
                "error": (
                    {
                        "message": span_db.status.error.message,
                        "stacktrace": span_db.status.error.stacktrace,
                    }
                    if span_db.status.value == "FAILURE"
                    else None
                ),
            },
            "metadata": span_db.meta,
            "user_id": str(user.id),
        },
        **{
            "span_id": str(span_db.id),
            "content": {
                "inputs": span_db.inputs,
                "output": span_db.outputs[0],
            },
            "model_params": {
                "prompt": {
                    "system": (span_db.prompt_system),
                    "user": span_db.prompt_user,
                    "variables": convert_variables(span_db),
                },
                "params": app_variant_db.config.parameters,
            },
        },
    )


async def retrieve_observability_dashboard(
    params: ObservabilityDashboardDataRequestParams,
) -> ObservabilityDashboardData:
    traces = await TraceDB.find(TraceDB.app_id == ObjectId(params.appId))
    list_of_spans_db: SpanDB = []

    for trace in traces:
        for span in trace.spans:
            span_db = await SpanDB.find_one(SpanDB.id == ObjectId(span))
            list_of_spans_db.append(span_db)

    list_of_observability_data: ObservabilityData = []
    for span_db in list_of_spans_db:
        list_of_observability_data.append(
            ObservabilityData(
                **{
                    "timestamp": span_db.created_at,
                    "success_count": len(list_of_spans_db),
                    "failure_count": 0,
                    "cost": span_db.cost,
                    "latency": span_db.latency,
                    "total_tokens": span_db.token_total,
                    "prompt_tokens": span_db.tokens_input,
                    "completion_tokens": span_db.tokens_output,
                    "environment": "",
                    "variant": "",
                }
            )
        )

    def filter_data(data: ObservabilityData):
        if params:
            if params.environment and data.environment == params.environment:
                return True
            if params.variant and data.variant == params.variant:
                return True

            # Convert data.timestamp to epoch time
            epoch_time = int(data.timestamp.timestamp())
            if (params.startTime and params.endTime) and (
                epoch_time in [params.startTime, params.endTime]
            ):
                return True
            if (
                params.environment == data.environment
                and params.variant == data.variant
            ):
                return True
            if (
                (params.startTime and params.endTime)
                and (data.timestamp in [params.startTime, params.endTime])
                and (
                    params.environment == data.environment
                    and params.variant == data.variant
                )
            ):
                return True
        return False

    len_of_spans_db = len(list_of_observability_data)
    filtered_data = filter(filter_data, list_of_observability_data)
    return ObservabilityDashboardData(
        **{
            "data": list(filtered_data),
            "total_count": len_of_spans_db,
            "failure_rate": 0,
            "total_cost": sum([span_db.cost for span_db in list_of_spans_db]),
            "avg_cost": sum([span_db.cost for span_db in list_of_spans_db])
            / len_of_spans_db,
            "avg_latency": sum([span_db.duration for span_db in list_of_spans_db])
            / len_of_spans_db,
            "total_tokens": sum([span_db.token_total for span_db in list_of_spans_db]),
            "avg_tokens": sum([span_db.token_total for span_db in list_of_spans_db])
            / len_of_spans_db,
        }
    )


async def delete_span(span_id: str):
    """Delete the span for a given span_id.

    Args:
        span_id (str): The Id of the span
    """

    span = await SpanDB.find_one(SpanDB.id == ObjectId(span_id))
    await span.delete()


async def add_feedback_to_trace(
    trace_id: str, payload: CreateFeedback, user_uid: str
) -> str:
    """Add a feedback to a trace.

    Args:
        trace_id (str): the Id of the trace
        payload (CreateFeedback): the required payload

    Returns:
        str: the feedback id
    """

    user = await db_manager.get_user(user_uid)
    feedback = FeedbackDB(
        user_id=str(user.id),
        feedback=payload.feedback,
        score=payload.score,
        created_at=datetime.now(),
    )

    trace = await TraceDB.find_one(TraceDB.id == ObjectId(trace_id), fetch_links=True)
    if trace.feedbacks is None:
        trace.feedbacks = [feedback]
    else:
        trace.feedbacks.append(feedback)

    # Update trace
    await trace.save()
    return feedback.uid


async def get_trace_feedbacks(trace_id: str, user_uid: str) -> List[Feedback]:
    """Get the feedbacks for a given trace.

    Args:
        trace_id (str): the Id of the trace

    Returns:
        List[Feedback]: the list of feedbacks for the given trace
    """

    user = await db_manager.get_user(user_uid)

    # Get feedbacks in trace
    trace = await TraceDB.find_one(
        TraceDB.id == ObjectId(trace_id), TraceDB.user.id == user.id, fetch_links=True
    )
    feedbacks = [feedback_db_to_pydantic(feedback) for feedback in trace.feedbacks]
    return feedbacks


async def get_feedback_detail(
    trace_id: str, feedback_id: str, user_uid: str
) -> Feedback:
    """Get a single feedback.

    Args:
        trace_id (str): the Id of the trace
        feedback_id (str): the Id of the feedback

    Returns:
        Feedback: the feedback
    """

    user = await db_manager.get_user(user_uid)

    # Get trace
    trace = await TraceDB.find_one(
        TraceDB.id == ObjectId(trace_id), TraceDB.user.id == user.id, fetch_links=True
    )

    # Get feedback
    feedback = [
        feedback_db_to_pydantic(feedback)
        for feedback in trace.feedbacks
        if feedback.uid == feedback_id
    ]
    return feedback[0]


async def update_trace_feedback(
    trace_id: str, feedback_id: str, payload: UpdateFeedback, user_uid: str
) -> Feedback:
    """Update a feedback.

    Args:
        trace_id (str): the Id of the trace
        feedback_id (str): the Id of the feedback
        payload (UpdateFeedback): the required payload

    Returns:
        Feedback: the feedback
    """

    user = await db_manager.get_user(user_uid)

    # Get trace
    trace = await TraceDB.find_one(
        TraceDB.id == ObjectId(trace_id), TraceDB.user.id == user.id, fetch_links=True
    )

    # update feedback
    feedback_json = {}
    for feedback in trace.feedbacks:
        if feedback.uid == feedback_id:
            for key, value in payload.dict(exclude_none=True).items():
                setattr(feedback, key, value)
            feedback_json = feedback.dict()
            break

    # Save feedback in trace and return a copy
    await trace.save()

    # Replace key and transform into a pydantic representation
    feedback_json["feedback_id"] = feedback_json.pop("uid")
    return Feedback(**feedback_json)
