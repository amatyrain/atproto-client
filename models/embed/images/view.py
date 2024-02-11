import dataclasses
from ....models.embed.images.aspect_ratio import AspectRatio


# ref: https://github.com/bluesky-social/atproto/blob/main/lexicons/app/bsky/embed/images.json
@dataclasses.dataclass
class View():
    thumb: str | None = None
    fullsize: str | None = None
    alt: str | None = None
    aspectRatio: AspectRatio | None = None
