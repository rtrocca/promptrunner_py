from enum import Enum

class ResultType(str, Enum):
    TEXT = "text"
    OBJECT = "object"
    ERROR = "error"
