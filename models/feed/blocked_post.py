import dataclasses


@dataclasses.dataclass
class BlockedPost():
    uri: str
    author: dict
    blocked: bool = True
