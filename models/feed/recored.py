from pydantic import BaseModel

from libs.atproto.models.embed.external.view import View
from libs.atproto.models.richtext.facet.facet import Facet


class Record(BaseModel):
    text: str
    created_at: str
    embed: View | None = None
    facets: list[Facet] | None = None
