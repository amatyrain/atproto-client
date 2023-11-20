import dataclasses
from libs.atproto.models.richtext.facet.byte_slice import ByteSlice
from libs.atproto.models.richtext.facet.link import Link


@dataclasses.dataclass
class Facet():
    # "index": { "type": "ref", "ref": "#byteSlice" },
    index: ByteSlice | None = None
    # "features": {
    #   "type": "array",
    #   "items": { "type": "union", "refs": ["#mention", "#link", "#tag"] }
    # }
    features: list[Link] | None = None
