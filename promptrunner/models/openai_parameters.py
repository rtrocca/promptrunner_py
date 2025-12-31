from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from .output_type import OutputType

class OpenAIParameters(BaseModel):
    max_tokens: Optional[int] = Field(None, alias="max-tokens")
    #GPT 5.0 needs max_completion_tokens, while older models use max_tokens
    max_completion_tokens: Optional[int] = Field(None, alias="max-completion-tokens")
    temperature: Optional[float] = None
    output_type: OutputType = Field(OutputType.TEXT, alias="output-type")
    json_schema: Optional[Dict[str, Any]] = Field(None, alias="json-schema")
