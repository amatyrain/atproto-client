import dataclasses
from libs.atproto.models.embed.external.view import View
from libs.atproto.models.richtext.facet.facet import Facet


@dataclasses.dataclass
class Record():
    text: str
    created_at: str
    embed: View | None = None
    facets: list[Facet] | None = None
