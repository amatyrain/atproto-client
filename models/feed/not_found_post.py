from pydantic import BaseModel


class NotFoundPost(BaseModel):
    uri: str
    notFound: bool = True
