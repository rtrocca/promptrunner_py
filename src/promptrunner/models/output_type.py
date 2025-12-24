from enum import Enum

class OutputType(str, Enum):
    TEXT = "text"
    JSON = "json"
    JSON_SCHEMA = "json-schema"
