from enum import Enum

class Role(str, Enum):
    SYSTEM = "system"
    ASSISTANT = "assistant"
    USER = "user"
    HISTORY = "history" # for including past interactions
