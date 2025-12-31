from typing import Dict, Any, Optional
from pybars import Compiler
from .interfaces import PromptLoader, ModelConfiguration
from .models.result import Result
from .models.result_type import ResultType
from .models.message import Message
from .models.model_type import ModelType
from .drivers.openai_driver import OpenAIDriver

class PromptRunner:
    def __init__(self, prompt_loader: PromptLoader, model_config: ModelConfiguration):
        self.prompt_loader = prompt_loader
        self.model_config = model_config
        self.compiler = Compiler()
        self._drivers = {
            ModelType.OPENAI: OpenAIDriver()
        }

    def run(self, prompt_name: str, variables: Dict[str, Any], overrides: Optional[Dict[str, Any]] = None) -> Result:
        """
        Runs the specified prompt with the given variables.
        """
        # 1. Get prompt from loader
        original_prompt = self.prompt_loader.get_prompt(prompt_name)
        prompt = original_prompt.model_copy(deep=True)

        # Apply overrides
        if overrides:
            if "model" in overrides:
                prompt.model = overrides["model"]
            if "parameters" in overrides:
                if prompt.parameters is None:
                    prompt.parameters = {}
                prompt.parameters.update(overrides["parameters"])
                print(prompt.parameters)
        
        # 2. Get model definition from config
        model_def = self.model_config.get_model(prompt.model)
        
        # 3. Render messages
        rendered_messages = []
        for msg in prompt.messages:
            template = self.compiler.compile(msg.content)
            rendered_content = template(variables)
            rendered_messages.append(Message(role=msg.role, content=rendered_content))
            
        # 4. Get driver
        driver = self._drivers.get(model_def.model_type)
        if not driver:
             return Result(type=ResultType.ERROR, content=f"No driver found for model type: {model_def.model_type}")

        # 5. Execute
        return driver.execute(prompt, rendered_messages, model_def)
