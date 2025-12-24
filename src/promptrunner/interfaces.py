from abc import ABC, abstractmethod
from .models import Prompt, ModelDefinition

class PromptLoader(ABC):
    @abstractmethod
    def get_prompt(self, name: str) -> Prompt:
        """
        Retrieves a prompt template by its name.
        """
        pass

class ModelConfiguration(ABC):
    @abstractmethod
    def get_model(self, model_id: str) -> ModelDefinition:
        """
        Retrieves a model definition by its unique ID.
        """
        pass
