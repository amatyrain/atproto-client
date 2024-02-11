import dataclasses


# ref: https://github.com/bluesky-social/atproto/blob/main/lexicons/app/bsky/embed/images.json
@dataclasses.dataclass
class AspectRatio():
    height: int | None = None
    width: int | None = None
