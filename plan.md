PromptRunner is a Python library that allows to run LLM prompts.
Prompts are specified using a YAML file.
For each prompt it's possible to specify:
- name
- version
- model (the name of the LLM model to use)

then a dictionary or parameters that depend on the model type (we need to plan for having not only OpenAI models, even if they will be the only ones right now)
In case of OpenAI the paremeters dictionary will be:
parameters:
    max-tokens: number of max tokens
    temperature: model temperature
    output-type: text|json|json-schema
    json-schema: if the output-type is json-schema here there will be the json-schema to be used in the API call

then there will be the "messages" property:
messages:
   - role: system|assistant|user
     content: <text content>
    
    - role: assistant
      content: ....

etc.
messages will be handlebars templates. Each message will be rendered with handlebars before being passed to the model.

The PromptRunner class will use a PromptLoader class.
The caller of PromptRunner can instantiate a PromptRunner instance passing, as a parameter the PromptLoader
PromptLoader will take care of retrieving a prompt template, given a name.
The PromptClient will also take a ModelConfiguration file as parameter.
We will create a YAMLPromptLoader, that will load a multi document YAML and enable access to one of the prompts and a YAMLModelConfiguration that will read a multi document YAML file with the model definitions.

A model definition consits of:
- id: a unique id that will be used in the model property of PromptLoader
- model-type: OpenAI (for now the only value)
- model-name: the name of the model to be used in the API
- model-version: optional, the API/model version. This makes sense only for OpenAI right now.

The user can do something like this:
pc = PromptRunner(YAMLPromptLoader('prompts.yaml'), YAMLModelConfiguration('models.yaml))

result = pc.run('prompt_id', {param1: '...', param2: '...   ', ...})
result is an object with two properties:
- type (text, object, error)
- content: either text or an object
In case of error content contains an exception object.

The source code you create must be fully typed with typings and/or Pydantic.
Create also a run.py file that can be used to run a prompt.
run.py will take as parameters the name of a prompt and a string, expressed in JSON, with the paramters.
It will also use loadenv to load a .env file with paramters like the OpenAI API keys

The project MUST have unit tests.
After making changes run the unit tests.
Now as a first step, create classes, interfaces and unit tests without creating the code within. I want to evaluate the design you will create before you proceed with implementation



