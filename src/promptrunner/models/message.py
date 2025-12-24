from pydantic import BaseModel
from .role import Role

class Message(BaseModel):
    role: Role
    content: str
