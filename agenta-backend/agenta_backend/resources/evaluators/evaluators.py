rag_evaluator_settings_template = {
    "question_key": {
        "label": "Question Key",
        "default": "",
        "type": "string",
        "required": True,
        "advanced": False,
        "description": "The input question to the LLM application. This is the question used to retrieve the context and formulate the answer.",
    },
    "answer_key": {
        "label": "Answer Key",
        "default": "",
        "type": "string",
        "required": True,
        "advanced": False,
        "description": "The output answer generated by the LLM application. This should point to the answer formulated based on the input question and the retrieved context.",
    },
    "contexts_key": {
        "label": "Contexts Key",
        "default": "",
        "type": "string",
        "required": True,
        "advanced": False,
        "description": "The documents or snippets retrieved by the LLM application in the RAG workflow. These contexts are used to assess the faithfulness of the generated answer.",
    },
}
evaluators = [
    {
        "name": "Exact Match",
        "key": "auto_exact_match",
        "direct_use": True,
        "settings_template": {
            "correct_answer_key": {
                "label": "Expected Answer Column",
                "default": "correct_answer",
                "type": "string",
                "advanced": True,  # Tells the frontend that this setting is advanced and should be hidden by default
                "ground_truth_key": True,  # Tells the frontend that is the name of the column in the test set that should be shown as a ground truth to the user
                "description": "The name of the column in the test data that contains the correct answer",
            },
        },
        "description": "Exact Match evaluator determines if the output exactly matches the specified correct answer, ensuring precise alignment with expected results.",
        "oss": True,
    },
    {
        "name": "Contains Json",
        "key": "auto_contains_json",
        "direct_use": True,
        "settings_template": {},
        "description": "Contains Json evaluator checks if the output contains the specified JSON structure.",
        "oss": True,
    },
    {
        "name": "Similarity Match",
        "key": "auto_similarity_match",
        "direct_use": False,
        "settings_template": {
            "similarity_threshold": {
                "label": "Similarity Threshold",
                "type": "number",
                "default": 0.5,
                "description": "The threshold value for similarity comparison",
                "min": 0,
                "max": 1,
                "required": True,
            },
            "correct_answer_key": {
                "label": "Expected Answer Column",
                "default": "correct_answer",
                "type": "string",
                "advanced": True,  # Tells the frontend that this setting is advanced and should be hidden by default
                "ground_truth_key": True,  # Tells the frontend that is the name of the column in the test set that should be shown as a ground truth to the user
                "description": "The name of the column in the test data that contains the correct answer",
            },
        },
        "description": "Similarity Match evaluator checks if the generated answer is similar to the expected answer. You need to provide the similarity threshold. It uses the Jaccard similarity to compare the answers.",
        "oss": True,
    },
    {
        "name": "Semantic Similarity Match",
        "key": "auto_semantic_similarity",
        "direct_use": False,
        "description": "Semantic Similarity Match evaluator measures the similarity between two pieces of text by analyzing their meaning and context. It compares the semantic content, providing a score that reflects how closely the texts match in terms of meaning, rather than just exact word matches.",
        "settings_template": {
            "correct_answer_key": {
                "label": "Expected Answer Column",
                "default": "correct_answer",
                "type": "string",
                "advanced": True,  # Tells the frontend that this setting is advanced and should be hidden by default
                "ground_truth_key": True,  # Tells the frontend that is the name of the column in the test set that should be shown as a ground truth to the user
                "description": "The name of the column in the test data that contains the correct answer",
            },
        },
        "oss": True,
    },
    {
        "name": "Regex Test",
        "key": "auto_regex_test",
        "direct_use": False,
        "description": "Regex Test evaluator checks if the generated answer matches a regular expression pattern. You need to provide the regex expression and specify whether an answer is correct if it matches or does not match the regex.",
        "settings_template": {
            "regex_pattern": {
                "label": "Regex Pattern",
                "type": "regex",
                "default": "",
                "description": "Pattern for regex testing (ex: ^this_word\\d{3}$)",
                "required": True,
            },
            "regex_should_match": {
                "label": "Match/Mismatch",
                "type": "boolean",
                "default": True,
                "description": "If the regex should match or mismatch",
            },
        },
        "oss": True,
    },
    {
        "name": "JSON Field Match",
        "key": "field_match_test",
        "direct_use": False,
        "settings_template": {
            "json_field": {
                "label": "JSON Field",
                "type": "string",
                "default": "",
                "description": "The name of the field in the JSON output that you wish to evaluate",
                "required": True,
            },
            "correct_answer_key": {
                "label": "Expected Answer Column",
                "default": "correct_answer",
                "type": "string",
                "advanced": True,  # Tells the frontend that this setting is advanced and should be hidden by default
                "ground_truth_key": True,  # Tells the frontend that is the name of the column in the test set that should be shown as a ground truth to the user
                "description": "The name of the column in the test data that contains the correct answer",
            },
        },
        "description": "JSON Field Match evaluator compares specific fields within JSON (JavaScript Object Notation) data. This matching can involve finding similarities or correspondences between fields in different JSON objects.",
        "oss": True,
    },
    {
        "name": "JSON Diff Match",
        "key": "auto_json_diff",
        "direct_use": False,
        "description": "JSON Diff evaluator compares two JSON objects to identify differences. It highlights discrepancies, additions, deletions, and modifications between the objects, providing a clear report of how they differ.",
        "settings_template": {
            "compare_schema_only": {
                "label": "Compare Schema Only",
                "type": "boolean",
                "default": False,
                "advanced": True,
                "description": "If set to True, we will compare the keys and the values type. Otherwise, we will compare the keys, the values and the values type.",
            },
            "predict_keys": {
                "label": "Include prediction keys",
                "type": "boolean",
                "default": False,
                "advanced": True,
                "description": "If set to True, we will check the reference (ground truth) keys. Othwerise, we will check both the reference (ground truth) and prediction (app output) keys.",
            },
            "case_insensitive_keys": {
                "label": "Enable Case-sensitive keys",
                "type": "boolean",
                "default": False,
                "advanced": True,
                "description": "If set to True, we will treat keys as case-insensitive, meaning 'key', 'Key', and 'KEY' would all be considered equivalent. Otherwise, we will not.",
            },
            "correct_answer_key": {
                "label": "Expected Answer Column",
                "default": "correct_answer",
                "type": "string",
                "advanced": True,  # Tells the frontend that this setting is advanced and should be hidden by default
                "ground_truth_key": True,  # Tells the frontend that is the name of the column in the test set that should be shown as a ground truth to the user
                "description": "The name of the column in the test data that contains the correct answer",
            },
        },
        "oss": True,
    },
    {
        "name": "AI Critique",
        "key": "auto_ai_critique",
        "direct_use": False,
        "settings_template": {
            "prompt_template": {
                "label": "Prompt Template",
                "type": "text",
                "default": "We have an LLM App that we want to evaluate its outputs. Based on the prompt and the parameters provided below evaluate the output based on the evaluation strategy below:\nEvaluation strategy: 0 to 10 0 is very bad and 10 is very good.\nPrompt: {llm_app_prompt_template}\nInputs: country: {country}\nExpected Answer Column:{correct_answer}\nEvaluate this: {variant_output}\n\nAnswer ONLY with one of the given grading or evaluation options.",
                "description": "Template for AI critique prompts",
                "required": True,
            },
            "correct_answer_key": {
                "label": "Expected Answer Column",
                "default": "correct_answer",
                "type": "string",
                "advanced": True,  # Tells the frontend that this setting is advanced and should be hidden by default
                "ground_truth_key": True,  # Tells the frontend that is the name of the column in the test set that should be shown as a ground truth to the user
                "description": "The name of the column in the test data that contains the correct answer",
            },
        },
        "description": "AI Critique evaluator sends the generated answer and the correct_answer to an LLM model and uses it to evaluate the correctness of the answer. You need to provide the evaluation prompt (or use the default prompt).",
        "oss": True,
    },
    {
        "name": "Code Evaluation",
        "key": "auto_custom_code_run",
        "direct_use": False,
        "settings_template": {
            "code": {
                "label": "Evaluation Code",
                "type": "code",
                "default": "from typing import Dict\n\ndef evaluate(\n    app_params: Dict[str, str],\n    inputs: Dict[str, str],\n    output: str, # output of the llm app\n    datapoint: Dict[str, str] # contains the testset row \n) -> float:\n    if output in datapoint.get('correct_answer', None):\n        return 1.0\n    else:\n        return 0.0\n",
                "description": "Code for evaluating submissions",
                "required": True,
            },
            "correct_answer_key": {
                "label": "Expected Answer Column",
                "default": "correct_answer",
                "type": "string",
                "advanced": True,  # Tells the frontend that this setting is advanced and should be hidden by default
                "ground_truth_key": True,  # Tells the frontend that is the name of the column in the test set that should be shown as a ground truth to the user
                "description": "The name of the column in the test data that contains the correct answer. This will be shown in the results page.",
            },
        },
        "description": "Code Evaluation allows you to write your own evaluator in Python. You need to provide the Python code for the evaluator.",
        "oss": True,
    },
    {
        "name": "Webhook test",
        "key": "auto_webhook_test",
        "direct_use": False,
        "settings_template": {
            "webhook_url": {
                "label": "Webhook URL",
                "type": "string",
                "description": "https://your-webhook-url.com",
                "required": True,
            },
            "correct_answer_key": {
                "label": "Expected Answer Column",
                "default": "correct_answer",
                "type": "string",
                "advanced": True,  # Tells the frontend that this setting is advanced and should be hidden by default
                "ground_truth_key": True,  # Tells the frontend that is the name of the column in the test set that should be shown as a ground truth to the user
                "description": "The name of the column in the test data that contains the correct answer",
            },
        },
        "description": "Webhook test evaluator sends the generated answer and the correct_answer to a webhook and expects a response, in JSON format, indicating the correctness of the answer, along with a 200 HTTP status. You need to provide the URL of the webhook and the response of the webhook must be between 0 and 1.",
        "oss": True,
    },
    {
        "name": "Starts With",
        "key": "auto_starts_with",
        "direct_use": False,
        "settings_template": {
            "prefix": {
                "label": "prefix",
                "type": "string",
                "required": True,
                "description": "The string to match at the start of the output.",
            },
            "case_sensitive": {
                "label": "Case Sensitive",
                "type": "boolean",
                "default": True,
                "description": "If the evaluation should be case sensitive.",
            },
        },
        "description": "Starts With evaluator checks if the output starts with a specified prefix, considering case sensitivity based on the settings.",
        "oss": True,
    },
    {
        "name": "Ends With",
        "key": "auto_ends_with",
        "direct_use": False,
        "settings_template": {
            "case_sensitive": {
                "label": "Case Sensitive",
                "type": "boolean",
                "default": True,
                "description": "If the evaluation should be case sensitive.",
            },
            "suffix": {
                "label": "suffix",
                "type": "string",
                "description": "The string to match at the end of the output.",
                "required": True,
            },
        },
        "description": "Ends With evaluator checks if the output ends with a specified suffix, considering case sensitivity based on the settings.",
        "oss": True,
    },
    {
        "name": "Contains",
        "key": "auto_contains",
        "direct_use": False,
        "settings_template": {
            "case_sensitive": {
                "label": "Case Sensitive",
                "type": "boolean",
                "default": True,
                "description": "If the evaluation should be case sensitive.",
            },
            "substring": {
                "label": "substring",
                "type": "string",
                "description": "The string to check if it is contained in the output.",
                "required": True,
            },
        },
        "description": "Contains evaluator checks if the output contains a specified substring, considering case sensitivity based on the settings.",
        "oss": True,
    },
    {
        "name": "Contains Any",
        "key": "auto_contains_any",
        "direct_use": False,
        "settings_template": {
            "case_sensitive": {
                "label": "Case Sensitive",
                "type": "boolean",
                "default": True,
                "description": "If the evaluation should be case sensitive.",
            },
            "substrings": {
                "label": "substrings",
                "type": "string",
                "description": "Provide a comma-separated list of strings to check if any is contained in the output.",
                "required": True,
            },
        },
        "description": "Contains Any evaluator checks if the output contains any of the specified substrings from a comma-separated list, considering case sensitivity based on the settings.",
        "oss": True,
    },
    {
        "name": "Contains All",
        "key": "auto_contains_all",
        "direct_use": False,
        "settings_template": {
            "case_sensitive": {
                "label": "Case Sensitive",
                "type": "boolean",
                "default": True,
                "description": "If the evaluation should be case sensitive.",
            },
            "substrings": {
                "label": "substrings",
                "type": "string",
                "description": "Provide a comma-separated list of strings to check if all are contained in the output.",
                "required": True,
            },
        },
        "description": "Contains All evaluator checks if the output contains all of the specified substrings from a comma-separated list, considering case sensitivity based on the settings.",
        "oss": True,
    },
    {
        "name": "Levenshtein Distance",
        "key": "auto_levenshtein_distance",
        "direct_use": False,
        "settings_template": {
            "threshold": {
                "label": "Threshold",
                "type": "number",
                "required": False,
                "description": "The maximum allowed Levenshtein distance between the output and the correct answer.",
            },
            "correct_answer_key": {
                "label": "Expected Answer Column",
                "default": "correct_answer",
                "type": "string",
                "advanced": True,  # Tells the frontend that this setting is advanced and should be hidden by default
                "ground_truth_key": True,  # Tells the frontend that is the name of the column in the test set that should be shown as a ground truth to the user
                "description": "The name of the column in the test data that contains the correct answer",
            },
        },
        "description": "This evaluator calculates the Levenshtein distance between the output and the correct answer. If a threshold is provided in the settings, it returns a boolean indicating whether the distance is within the threshold. If no threshold is provided, it returns the actual Levenshtein distance as a numerical value.",
        "oss": True,
    },
    {
        "name": "RAG Faithfulness",
        "key": "rag_faithfulness",
        "direct_use": False,
        "settings_template": rag_evaluator_settings_template,
        "description": "RAG Faithfulness evaluator assesses the accuracy and reliability of responses generated by Retrieval-Augmented Generation (RAG) models. It evaluates how faithfully the responses adhere to the retrieved documents or sources, ensuring that the generated text accurately reflects the information from the original sources.",
    },
    {
        "name": "RAG Context Relevancy",
        "key": "rag_context_relevancy",
        "direct_use": False,
        "settings_template": rag_evaluator_settings_template,
        "description": "RAG Context Relevancy evaluator measures how relevant the retrieved documents or contexts are to the given question or prompt. It ensures that the selected documents provide the necessary information for generating accurate and meaningful responses, improving the overall quality of the RAG model's output.",
    },
]


def get_all_evaluators():
    """
    Returns a list of evaluators

    Returns:
        List[dict]: A list of evaluator dictionaries.
    """
    return evaluators
