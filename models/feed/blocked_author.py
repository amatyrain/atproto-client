from pydantic import BaseModel


class blockedAuthor(BaseModel):
    uri: str
    blocked: bool = True
    author: dict
