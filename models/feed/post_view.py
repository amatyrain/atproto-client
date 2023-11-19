import dataclasses
from libs.atproto.models.embed.external.view import View
from libs.atproto.models.feed.recored import Record


# DTOクラス定義
@dataclasses.dataclass
class PostView():
    cid: str
    record: Record | None = None
    embed: View | None = None
