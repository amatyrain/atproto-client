import dataclasses
from ...models.feed.blocked_post import BlockedPost
from ...models.feed.not_found_post import NotFoundPost
from ...models.feed.post_view import PostView


@dataclasses.dataclass
class ReplyRef():
    root: PostView | NotFoundPost | BlockedPost | None = None
    parent: PostView | NotFoundPost | BlockedPost | None = None
