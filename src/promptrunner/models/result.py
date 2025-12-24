from typing import Union, Dict, Any
from pydantic import BaseModel
from .result_type import ResultType

class Result(BaseModel):
    type: ResultType
    content: Union[str, Dict[str, Any], Any] 
    
    class Config:
        arbitrary_types_allowed = True
