import yaml
from typing import Dict
from ..interfaces import ModelConfiguration
from ..models import ModelDefinition

class YAMLModelConfiguration(ModelConfiguration):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._models: Dict[str, ModelDefinition] = self._load_models()

    def _load_models(self) -> Dict[str, ModelDefinition]:
        models = {}
        with open(self.file_path, 'r') as f:
            documents = yaml.safe_load_all(f)
            for doc in documents:
                if not doc:
                    continue
                if isinstance(doc, list):
                    for item in doc:
                        model = ModelDefinition(**item)
                        models[model.id] = model
                else:
                    model = ModelDefinition(**doc)
                    models[model.id] = model
        return models

    def get_model(self, model_id: str) -> ModelDefinition:
        if model_id not in self._models:
            raise ValueError(f"Model '{model_id}' not found in {self.file_path}")
        return self._models[model_id]
