import json

from langchain.tools import tool


@tool
def search_tirith_example_tool(query: str) -> str:
    """
    Search for a Tirith policy example.
    The input is a description of a tirith example you want to fetch.
    """
    return """
{
    "meta": {
        "version": "v1",
        "required_provider": "stackguardian/terraform_plan"
    },
    "evaluators": [
        {
            "id": "ec2_depends_on_s3",
            "description": "Make sure that EC2 instances have explicit dependency on S3 bucket",
            "provider_args": {
                "operation_type": "direct_dependencies",
                "terraform_resource_type": "aws_instance"
            },
            "condition": {
                "type": "Contains",
                "value": "aws_s3_bucket",
                "error_tolerance": 2
            }
        }
    ],
    "eval_expression": "ec2_depends_on_s3"
}
"""


@tool
def get_tirith_providers_tool() -> str:
    """
    Get all available tirith providers.
    """
    response = [
        {
            "name": "stackguardian/terraform_plan",
            "description": "A provider that allows you evalueate on terraform plan output",
            "version": "v1",
        },
        {
            "name": "stackguardian/infracost",
            "description": "A provider that allows you to evaluate on infracost result. Use this when you want to evaluate cost of your infrastructure",
        },
        {
            "name": "stackguardian/kubernetes",
            "description": "A provider that allows you to evaluate on kubernetes YAML configuration.",
        },
        {
            "name": "stackguardian/json",
            "description": "A provider that allows you to evaluate on JSON string",
        },
    ]
    return json.dumps(response)


@tool
def get_tirith_operation_types_tool(provider_name: str) -> str:
    """
    Get all available operation types for a provider.
    """
    operation_type_map = {
        "stackguardian/terraform_plan": [
            {
                "name": "attribute",
                "description": "Get the value of a specific attribute of a resource",
                "needed_args": {
                    "terraform_resource_type": {
                        "description": "The terraform resource type to get the attribute",
                        "tools": "search_terraform_resource_types_tool",
                    },
                    "terraform_resource_attribute": {
                        "description": "The attribute to get the value",
                        "tools": "search_terraform_attributes_tool",
                    },
                },
                "error_values": {
                    "1": "When a resource is not found",
                    "2": "When an attribute of a resource is not found",
                    "99": "Generic error for unsupported operations or invalid inputs",
                },
            },
            {
                "name": "action",
                "description": "Get actions performed on a resource",
                "needed_args": {
                    "terraform_resource_type": {
                        "description": "The terraform resource type to get the actions",
                        "tools": "search_terraform_resource_types_tool",
                    },
                },
                "error_values": {
                    "1": "When a resource is not found",
                    "99": "Generic error for unsupported operations or invalid inputs",
                },
            },
            {
                "name": "count",
                "description": "Get count of a particular resource",
                "needed_args": {
                    "terraform_resource_type": {
                        "description": "The terraform resource type to get the count",
                        "tools": "search_terraform_resource_types_tool",
                    },
                },
                "error_values": {
                    "99": "Generic error for unsupported operations or invalid inputs",
                },
            },
            {
                "name": "direct_dependencies",
                "description": "Get direct dependencies of a resource",
                "needed_args": {
                    "terraform_resource_type": {
                        "description": "The terraform resource type to get the direct dependencies",
                        "tools": "search_terraform_resource_types_tool",
                    },
                },
                "error_values": {
                    "99": "Generic error for unsupported operations or invalid inputs",
                },
            },
            {
                "name": "direct_references",
                "description": "Get direct references to or from a resource",
                "needed_args": {
                    "terraform_resource_type": {
                        "description": "The terraform resource type to get the direct references",
                        "tools": "search_terraform_resource_types_tool",
                    },
                    "referenced_by": {
                        "description": "The resource type that references the specified resource type",
                        "tools": "search_terraform_resource_types_tool",
                    },
                    "references_to": {
                        "description": "The resource type that the specified resource type references",
                        "tools": "search_terraform_resource_types_tool",
                    },
                },
                "error_values": {
                    "1": "When a resource is not found",
                    "99": "Generic error for unsupported operations or invalid inputs",
                },
            },
            {
                "name": "terraform_version",
                "description": "Get the Terraform version from the plan",
                "needed_args": {},
                "error_values": {
                    "99": "Generic error for unsupported operations or invalid inputs",
                },
            },
            {
                "name": "provider_config",
                "description": "Get the provider configuration from the plan",
                "needed_args": {
                    "terraform_provider_full_name": {
                        "description": "The full name of the Terraform provider",
                        "tools": "search_terraform_providers_tool",
                    },
                    "attribute": {
                        "description": "The attribute of the provider configuration to retrieve. Supported values: 'version_constraint', 'region'",
                        "tools": "search_provider_attributes_tool",
                    },
                },
                "error_values": {
                    "1": "When a resource is not found",
                    "2": "When an attribute of a resource is not found",
                    "99": "Generic error for unsupported operations or invalid inputs",
                },
            },
        ],
        "stackguardian/infracost": [
            {
                "name": "total_monthly_cost",
                "description": "Get the total monthly cost of all resources or specific resources",
                "needed_args": {
                    "resource_type": {
                        "description": "The type of the resource to calculate the cost for",
                        "tools": "search_resource_types_tool",
                    },
                    "operation_type": {
                        "description": "The type of cost operation to perform, e.g., 'total_monthly_cost'",
                        "tools": "search_cost_operations_tool",
                    },
                },
                "error_values": {
                    "1": "When a resource is not found",
                    "99": "Generic error for unsupported operations or invalid inputs",
                },
            },
            {
                "name": "total_hourly_cost",
                "description": "Get the total hourly cost of all resources or specific resources",
                "needed_args": {
                    "resource_type": {
                        "description": "The type of the resource to calculate the cost for",
                        "tools": "search_resource_types_tool",
                    },
                    "operation_type": {
                        "description": "The type of cost operation to perform, e.g., 'total_hourly_cost'",
                        "tools": "search_cost_operations_tool",
                    },
                },
                "error_values": {
                    "1": "When a resource is not found",
                    "99": "Generic error for unsupported operations or invalid inputs",
                },
            },
        ],
        "stackguardian/kubernetes": [
            {
                "name": "attribute",
                "description": "Get the value of a specific attribute of a Kubernetes resource",
                "needed_args": {
                    "kubernetes_kind": {
                        "description": "The Kubernetes resource kind to get the attribute from",
                        "tools": "search_kubernetes_resource_kinds_tool",
                    },
                    "attribute_path": {
                        "description": "The path to the attribute in the Kubernetes resource",
                        "tools": "search_kubernetes_attributes_tool",
                    },
                },
                "error_values": {
                    "1": "When a resource is not found",
                    "99": "Generic error for unsupported operations or invalid inputs",
                },
            },
        ],
        "stackguardian/json": [
            {
                "name": "get_value",
                "description": "Get the value from a dictionary based on the specified key path",
                "needed_args": {
                    "key_path": {
                        "description": "The path to the key in the input dictionary, separated by `.`, can also have `*` (wildcard). If `*` is provided, the returned value will be list",
                        "tools": "search_key_paths_tool",
                    },
                },
                "error_values": {
                    "2": "When the key path is not found",
                    "99": "Generic error for unsupported operations or invalid inputs",
                },
            },
        ],
    }

    return json.dumps(operation_type_map[provider_name])


# In the future, when the provider-provided condition types are already supported
# this will have a string parameter, like `provider_name: str`
# Optimization thoughts:
# - We can try to use csv instead of JSON format because JSON has a lot of overhead
#   and the structure of our response is always flat
#   OR even better, put it into a SQL db
#   See https://genai.stackexchange.com/questions/492/are-llms-in-particular-gpt3-5-4-better-at-interpreting-xml-or-json-for-input
@tool
def get_available_tirith_condition_types_tool():
    """Get available tirith condition types"""
    response = {
        "ContainedIn": {
            "description": "Checks if the given value is contained within a specified list or collection"
        },
        "Contains": {
            "description": "Checks if a specified list or collection contains the given value"
        },
        "Equals": {
            "description": "Checks if the given value is equal to a specified value"
        },
        "GreaterThanEqualTo": {
            "description": "Checks if the given value is greater than or equal to a specified value"
        },
        "GreaterThan": {
            "description": "Checks if the given value is greater than a specified value"
        },
        "IsEmpty": {
            "description": "Checks if the given value, list, or collection is empty"
        },
        "IsNotEmpty": {
            "description": "Checks if the given value, list, or collection is not empty"
        },
        "LessThanEqualTo": {
            "description": "Checks if the given value is less than or equal to a specified value"
        },
        "LessThan": {
            "description": "Checks if the given value is less than a specified value"
        },
        "RegexMatch": {
            "description": "Checks if the given value matches a specified regular expression pattern"
        },
        "NotEquals": {
            "description": "Checks if the given value is not equal to a specified value"
        },
        "NotContainedIn": {
            "description": "Checks if the given value is not contained within a specified list or collection"
        },
        "NotContains": {
            "description": "Checks if a specified list or collection does not contain the given value"
        },
    }
    return json.dumps(response)
