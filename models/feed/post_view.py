import dataclasses
from ...models.embed.external.view import View
from ...models.feed.recored import Record


# DTOクラス定義
@dataclasses.dataclass
class PostView():
    cid: str
    record: Record | None = None
    embed: View | None = None
