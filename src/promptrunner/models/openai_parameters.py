from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from .output_type import OutputType

class OpenAIParameters(BaseModel):
    max_tokens: Optional[int] = Field(None, alias="max-tokens")
    temperature: Optional[float] = None
    output_type: OutputType = Field(OutputType.TEXT, alias="output-type")
    json_schema: Optional[Dict[str, Any]] = Field(None, alias="json-schema")
