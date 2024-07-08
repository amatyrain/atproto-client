import dataclasses


@dataclasses.dataclass
class blockedAuthor():
    uri: str
    author: dict
    blocked: bool = True
