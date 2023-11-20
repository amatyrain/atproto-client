import dataclasses


@dataclasses.dataclass
class ReasonRepost():
    text: str
    created_at: str  # 2023-11-18T10:42:49.198Z
    cid: str
    parent_cid: str = ""
