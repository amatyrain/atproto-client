import dataclasses
from libs.atproto.models.feed.blocked_post import BlockedPost
from libs.atproto.models.feed.not_found_post import NotFoundPost
from libs.atproto.models.feed.post_view import PostView


@dataclasses.dataclass
class ReplyRef():
    root: PostView | NotFoundPost | BlockedPost | None = None
    parent: PostView | NotFoundPost | BlockedPost | None = None
