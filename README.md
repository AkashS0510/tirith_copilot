# Tirith Copilot

Tirith copilot is a LLM-based decision support system that can help its users
to create Tirith policy from the user input using natural language policy

## Architecture

Main chain structure:
1. Provider selection (router)
2. Provider specific chains

### Provider chains

#### Terraform Provider chain
1. Create the tirith policy
  - Tools:
    - `TerraformExpertAgent` that specializes on finding what `terraform_resource_type`
      and `terraform_resource_attribute` value/path to use
    - `ProblemDividerAgent` that divides the problem into multiple small problems
      in case the user has a request to make a tirith policy
      - I think we don't need this we can just add CoT prompt
    - `search_examples` that searches for examples of the user input

#### Infracost Provider chain
1. Create an outline of the evaluators (divide the problem into multiple small problems) and combine them
2. Create the tirith policy (TirithPolicyCreatorAgent)

#### Kubernetes Provider chain
1. Create an outline of the evaluators (divide the problem into multiple small problems) and combine them
2. Create the tirith policy

#### JSON Provider chain
1. Create an outline of the evaluators (divide the problem into multiple small problems) and combine them
2. Create the tirith policy


## Ideas
- Use multi-agent architecture
    - Add `TerraformExpertAgent` that specializes on finding what `terraform_resource_type`
      and `terraform_resource_attribute` value/path to use
      - It can send multiple values if it feels that it needs to limit more than one value
      - It will send back the resource_type and the resource_attribute and what
        value should it limit to. And then the `TirithExpert` agent will make the resource based on that
- Reducing the perplexity value of the prompts could be helpful
  - We might ask GPT to generate the prompt for us, and then we can use that
    prompt to generate the policy. This ensures that the model understand the prompt
    and thus lowering the perplexity value
  - Need to search for paper regarding this

## TODO:
- Implement the `TerraformExpert` agent
- Evaluation of the whole features
  - We can implement it like unit testing
  - We can also calculate the cost estimation from here
- Integrate with the tirith project, remove all of the hardcodes when we are sure
  that the prompt will work
  - Introduce provider and condition types schema to tirith project to make it easier
    for user to read the docs, and also for tirith copilot project to consume
    - Add return values for the `get_tirith_operation_types()`
- Calculate cost to release this to prod (Akshat)

## Tirith features coverage
- (DONE) Create basic tirith policy
- (DONE) Combine evaluators
- Skipping mechanism by using error tolerance
- Get the exact terraform resource name and attributes

## Evaluation strategy
- Use a pair of prompt and the policy to evaluate the model
- If the evaluation is expensive to do every time, we can do only spot checking for
  further continuous evaluation, but perhaps still have some mandatory test cases
- Incorporate Tirith in validating the JSON response
- See `evaluations.py` for the evaluation implementation

## Optimization comes last
- Please, please, please make a working prototype first, we'll think about the
optimization later, e.g. minimizing the number of intermediate steps, using
cheaper models, minimizing the number of tokens, etc

## Future
- When the Tirith project already has the docs, we can use GPT to just summarize
the docs and then, use it as the prompt to generate the policy
  - But we need the evaluation to be established first

## Dari Pak Dinar
- 19 Juni 2024
  - Perlu approval dari pakar Tirith (Akshat/Jo) untuk memvalidasi apakah
    hasil sudah sesuai atau tidak.
  - Inspirasi komparasi: app cursor.com
  - Compare performance between (need to think what will be the metric):
    - Using pure GPT memory
    - Using GPT with tools to eliminate hallucination (e.g. terraform_resource_type)
      - e.g. `get_terraform_resource_type()`

## 25 Juni 2024 thoughts
- Compare between:
  - Placing Tirith knowledge on basic functions vs placing it on vector db

## 25 July 2024
- For TerraformExpert, give one shot example and give it tools
  ```
  Give the user the resources and the attributes path to limit

  Example:
  I want to make s3 private

  Answer:
  resource_type: aws_s3_bucket
  resource_attribute: acl
  value: private

  and

  resource_type: aws_s3_bucket
  resource_attribute: block_public_acls
  value: true

  and
  resource_type: aws_s3_bucket
  resource_attribute: block_public_policy
  value: true
  ```

## 20 Aug 2024

- Frontend for the project: https://docs.chainlit.io/get-started/overview

# Steps
1. 
