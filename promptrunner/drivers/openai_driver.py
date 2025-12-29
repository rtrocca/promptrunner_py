import os
import json
from typing import List
from openai import OpenAI
from ..models.prompt import Prompt
from ..models.message import Message
from ..models.model_definition import ModelDefinition
from ..models.result import Result
from ..models.result_type import ResultType
from ..models.openai_parameters import OpenAIParameters
from ..models.output_type import OutputType
from .interfaces import LLMDriver

class OpenAIDriver(LLMDriver):
    def __init__(self):
        # We assume API key is in environment variables
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    def execute(self, prompt: Prompt, rendered_messages: List[Message], model_config: ModelDefinition) -> Result:
        # Parse parameters
        params_dict = prompt.parameters or {}
        openai_params = OpenAIParameters(**params_dict)

        # Prepare messages
        api_messages = []
        for msg in rendered_messages:
            # TODO: Handle Role.HISTORY if needed, for now we assume standard roles
            api_messages.append({
                "role": msg.role.value,
                "content": msg.content
            })

        # Prepare API call arguments
        kwargs = {
            "model": model_config.model_name,
            "messages": api_messages,
        }
        
        if openai_params.max_tokens:
            kwargs["max_tokens"] = openai_params.max_tokens
        
        if openai_params.temperature is not None:
            kwargs["temperature"] = openai_params.temperature

        # Handle response format (JSON mode)
        if openai_params.output_type == OutputType.JSON:
             kwargs["response_format"] = {"type": "json_object"}
        elif openai_params.output_type == OutputType.JSON_SCHEMA:
             if openai_params.json_schema:
                 kwargs["response_format"] = {
                     "type": "json_schema",
                     "json_schema": openai_params.json_schema
                 }

        try:
            response = self.client.chat.completions.create(**kwargs)
            content = response.choices[0].message.content

            if openai_params.output_type in (OutputType.JSON, OutputType.JSON_SCHEMA):
                try:
                    parsed_content = json.loads(content)
                    return Result(type=ResultType.OBJECT, content=parsed_content)
                except json.JSONDecodeError as e:
                    return Result(type=ResultType.ERROR, content=f"Failed to parse JSON response: {str(e)}\nResponse: {content}")
            
            return Result(type=ResultType.TEXT, content=content)

        except Exception as e:
            return Result(type=ResultType.ERROR, content=str(e))
