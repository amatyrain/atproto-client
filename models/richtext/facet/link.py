from pydantic import BaseModel


class Link(BaseModel):
    # "uri": { "type": "string", "format": "uri" }
    uri: str
