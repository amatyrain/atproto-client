import dataclasses
from libs.atproto.models.feed.post_view import PostView
from libs.atproto.models.feed.reply_ref import ReplyRef
from libs.atproto.models.feed.reason_repost import ReasonRepost


@dataclasses.dataclass
class FeedViewPost():
    post: PostView | None = None
    reply: ReplyRef | None = None
    reason: ReasonRepost | None = None
