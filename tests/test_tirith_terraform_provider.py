import json
import unittest

from langchain.evaluation import JsonSchemaEvaluator
from langchain.evaluation.parsing.json_schema import parse_json_markdown

from tirith_copilot.agent import main_chain

# Refer to link below for the reference
# https://python.langchain.com/v0.1/docs/guides/productionization/evaluation/
# Maybe we also need to use precision and accuracy metrics from the evaluation Hugging Face library

# TODO:
# - Use `JsonEvaluator` -- https://python.langchain.com/v0.1/docs/guides/productionization/evaluation/string/json/
# - Use `JsonSchemaEvaluator` -- https://python.langchain.com/v0.1/docs/guides/productionization/evaluation/string/json/#jsonschemaevaluator
# - Also consider Trajectory Evaluator so that we can make sure that the LLM is making tirith the right way


# Create a base class for the test later
class TirithTerraformProviderTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.agent_exc = main_chain
        cls.json_evaluator = JsonSchemaEvaluator()
        cls.json_schema = {
            "type": "object",
            "properties": {
                "meta": {
                    "type": "object",
                    "properties": {
                        "version": {"type": "string"},
                        "required_provider": {"type": "string"},
                    },
                    "required": ["version", "required_provider"],
                },
                "evaluators": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "description": {"type": "string"},
                            "provider_args": {
                                "type": "object",
                                "properties": {
                                    "operation_type": {"type": "string"},
                                },
                                "required": [
                                    "operation_type",
                                ],
                            },
                            "condition": {
                                "type": "object",
                                "properties": {
                                    "type": {"type": "string"},
                                    "value": {},
                                    "error_tolerance": {"type": "number"},
                                },
                                "required": ["type"]
                            },
                        },
                        "required": ["id", "description", "provider_args", "condition"],
                    },
                },
                "eval_expression": {"type": "string"},
            },
            "required": ["meta", "evaluators", "eval_expression"],
        }

    def assert_tirith_schema_is_valid(self, prediction: str):
        # Consider contributing this exception handling to the upstream
        try:
            result = self.json_evaluator.evaluate_strings(prediction=prediction, reference=self.json_schema)
        except json.decoder.JSONDecodeError as e:
            self.fail(f"Prediction is not a valid JSON: {e}\n\nPrediction:\n{prediction}\n")

        self.assertTrue(result["score"], f"Schema is invalid: {prediction}")

    def invoke_agent(self, input: str):
        return self.agent_exc.invoke(
            {
                "input": input,
                "chat_history": [],
            }
        )["output"]

    def test_create_s3_policy(self):
        prediction = self.invoke_agent("please create policy to limit s3 bucket public")
        self.assert_tirith_schema_is_valid(prediction)

        prediction_dict = parse_json_markdown(prediction)
        print(prediction_dict)
