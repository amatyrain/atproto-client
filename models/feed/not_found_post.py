import dataclasses


@dataclasses.dataclass
class NotFoundPost():
    uri: str
    notFound: bool = True
