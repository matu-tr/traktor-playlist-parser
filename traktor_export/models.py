from dataclasses import dataclass, field
from enum import Enum, auto


@dataclass
class Track:
    num: int
    title: str
    artist: str
    label: str | None = None
    bpm: float | None = None
    key: str | None = None


class Field(Enum):
    NUM = "num"
    TITLE = "title"
    ARTIST = "artist"
    LABEL = "label"
    BPM = "bpm"
    KEY = "key"


class FormatStyle(Enum):
    NUMBERED_LIST = auto()
    CUE_SHEET = auto()
    STANZA_BLOCK = auto()
    CUSTOM = auto()


class SourceKind(Enum):
    HTML = auto()
    NML = auto()


@dataclass
class ParseResult:
    tracks: list[Track]
    source_kind: SourceKind
    available_fields: set[Field]
    warnings: list[str] = field(default_factory=list)
