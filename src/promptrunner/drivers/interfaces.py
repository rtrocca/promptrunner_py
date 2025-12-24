from abc import ABC, abstractmethod
from typing import List
from ..models.prompt import Prompt
from ..models.message import Message
from ..models.model_definition import ModelDefinition
from ..models.result import Result

class LLMDriver(ABC):
    @abstractmethod
    def execute(self, prompt: Prompt, rendered_messages: List[Message], model_config: ModelDefinition) -> Result:
        """
        Executes the prompt using the specific LLM driver.
        """
        pass
