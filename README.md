# PromptRunner

PromptRunner is a Python library that allows you to run LLM prompts defined in YAML files. It supports templating using Handlebars and configuration of model parameters.

## Installation

1.  Clone the repository.
2.  Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3.  Create a `.env` file with your API keys (e.g., `OPENAI_API_KEY`).

## Usage

You can run prompts using the `run.py` script.

### Command Line Interface

```bash
python run.py <prompt_name> <params_json> [--prompts-file PROMPTS_FILE] [--models-file MODELS_FILE]
```

-   `prompt_name`: The name of the prompt to run (as defined in your prompts YAML file).
-   `params_json`: A JSON string containing the parameters to be passed to the prompt template.
-   `--prompts-file`: Path to the YAML file containing prompt definitions (default: `prompts.yaml`).
-   `--models-file`: Path to the YAML file containing model definitions (default: `models.yaml`).

### Example

Assuming you have a `prompts.yaml` and `models.yaml` configured (see below), you can run a prompt named `hello-world` like this:

```bash
python run.py hello-world '{"name": "Developer"}'
```

## Configuration Files

### models.yaml

Defines the available LLM models.

```yaml
- id: gpt-4-turbo
  model-type: OpenAI
  model-name: gpt-4-turbo-preview
  model-version: "2024-01-25"
```

### prompts.yaml

Defines the prompts, including their model configuration and message templates.

```yaml
- name: hello-world
  version: "1.0"
  model: gpt-4-turbo
  parameters:
    max-tokens: 100
    temperature: 0.7
    output-type: text
  messages:
    - role: system
      content: "You are a helpful assistant."
    - role: user
      content: "Hello, {{name}}!"
```
