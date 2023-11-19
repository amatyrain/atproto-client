import dataclasses


@dataclasses.dataclass
class ByteSlice():
    # "byteStart": { "type": "integer", "minimum": 0 },
    byteStart: int
    # "byteEnd": { "type": "integer", "minimum": 0 }
    byteEnd: int
