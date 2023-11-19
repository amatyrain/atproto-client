from pydantic import BaseModel


class viewerState(BaseModel):
    repost: str
    like: str
