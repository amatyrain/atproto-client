import dataclasses
from ...models.embed.external.view import View
from ...models.richtext.facet.facet import Facet


@dataclasses.dataclass
class Record():
    text: str
    created_at: str
    embed: View | None = None
    facets: list[Facet] | None = None
