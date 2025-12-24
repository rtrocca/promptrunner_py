import yaml
from typing import Dict
from ..interfaces import PromptLoader
from ..models import Prompt

class YAMLPromptLoader(PromptLoader):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._prompts: Dict[str, Prompt] = self._load_prompts()

    def _load_prompts(self) -> Dict[str, Prompt]:
        prompts = {}
        with open(self.file_path, 'r') as f:
            documents = yaml.safe_load_all(f)
            for doc in documents:
                if not doc:
                    continue
                if isinstance(doc, list):
                    for item in doc:
                        prompt = Prompt(**item)
                        prompts[prompt.name] = prompt
                else:
                    prompt = Prompt(**doc)
                    prompts[prompt.name] = prompt
        return prompts

    def get_prompt(self, name: str) -> Prompt:
        if name not in self._prompts:
            raise ValueError(f"Prompt '{name}' not found in {self.file_path}")
        return self._prompts[name]
