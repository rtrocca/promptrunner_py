from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from .message import Message

class Prompt(BaseModel):
    name: str
    version: str
    model: str  # This refers to the model ID in ModelDefinition
    parameters: Optional[Dict[str, Any]] = None
    messages: List[Message]
