import dataclasses


@dataclasses.dataclass
class BlockedPost():
    uri: str
    blocked: bool = True
    author: dict
