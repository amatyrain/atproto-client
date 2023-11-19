from pydantic import BaseModel


class BlockedPost(BaseModel):
    uri: str
    blocked: bool = True
    author: dict
