import dataclasses


@dataclasses.dataclass
class blockedAuthor():
    uri: str
    blocked: bool = True
    author: dict
