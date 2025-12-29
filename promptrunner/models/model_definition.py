from typing import Optional
from pydantic import BaseModel, Field
from .model_type import ModelType

class ModelDefinition(BaseModel):
    id: str
    model_type: ModelType = Field(..., alias="model-type")
    model_name: str = Field(..., alias="model-name")
    model_version: Optional[str] = Field(None, alias="model-version")
