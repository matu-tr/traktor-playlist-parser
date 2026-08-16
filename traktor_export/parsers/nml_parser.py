import xml.etree.ElementTree as ET

from ..models import Field, ParseResult, SourceKind, Track
from ..text_utils import remove_extended_mix
from .errors import ParseError
from .keycode import key_code_to_name


def _collection_key(entry: ET.Element) -> str | None:
    location = entry.find("LOCATION")
    if location is None:
        return None
    volume = location.get("VOLUME", "")
    dir_ = location.get("DIR", "")
    file_ = location.get("FILE", "")
    return f"{volume}{dir_}{file_}"


def _build_collection_index(root: ET.Element) -> dict[str, ET.Element]:
    collection = root.find("COLLECTION")
    if collection is None:
        raise ParseError("No <COLLECTION> found in NML file.")
    index: dict[str, ET.Element] = {}
    for entry in collection.findall("ENTRY"):
        key = _collection_key(entry)
        if key:
            index[key] = entry
    return index


def _find_playlist_nodes(root: ET.Element) -> list[ET.Element]:
    playlists = root.find("PLAYLISTS")
    if playlists is None:
        return []
    return [
        node
        for node in playlists.iter("NODE")
        if node.get("TYPE") == "PLAYLIST" and node.find("PLAYLIST") is not None
    ]


def list_playlist_names(path: str) -> list[str]:
    tree = ET.parse(path)
    root = tree.getroot()
    return [node.get("NAME", "") for node in _find_playlist_nodes(root)]


def parse_nml_playlist(path: str, playlist_name: str | None = None) -> ParseResult:
    try:
        tree = ET.parse(path)
    except ET.ParseError as exc:
        raise ParseError(f"Could not read NML file: {exc}") from exc
    root = tree.getroot()

    nodes = _find_playlist_nodes(root)
    if not nodes:
        raise ParseError("No playlist found in NML file.")

    if playlist_name is not None:
        matches = [n for n in nodes if n.get("NAME") == playlist_name]
        if not matches:
            raise ParseError(f"No playlist named '{playlist_name}' found.")
        node = matches[0]
    elif len(nodes) == 1:
        node = nodes[0]
    else:
        names = ", ".join(n.get("NAME", "") for n in nodes)
        raise ParseError(f"Multiple playlists found, one must be chosen: {names}")

    playlist = node.find("PLAYLIST")
    collection_index = _build_collection_index(root)

    tracks: list[Track] = []
    warnings: list[str] = []
    has_bpm = False
    has_key = False

    for i, entry_ref in enumerate(playlist.findall("ENTRY"), start=1):
        primary_key = entry_ref.find("PRIMARYKEY")
        if primary_key is None:
            warnings.append(f"Entry {i}: missing PRIMARYKEY, skipped.")
            continue
        key = primary_key.get("KEY", "")
        entry = collection_index.get(key)
        if entry is None:
            warnings.append(f"Entry {i}: no matching track in collection, skipped ({key}).")
            continue

        tempo = entry.find("TEMPO")
        bpm = None
        if tempo is not None and tempo.get("BPM") is not None:
            try:
                bpm = round(float(tempo.get("BPM")), 1)
                has_bpm = True
            except ValueError:
                pass

        musical_key = entry.find("MUSICAL_KEY")
        key_name = None
        if musical_key is not None and musical_key.get("VALUE") is not None:
            try:
                key_name = key_code_to_name(int(musical_key.get("VALUE")))
                has_key = True
            except ValueError:
                pass

        tracks.append(
            Track(
                num=len(tracks) + 1,
                title=remove_extended_mix(entry.get("TITLE", "")),
                artist=entry.get("ARTIST", ""),
                label=None,
                bpm=bpm,
                key=key_name,
            )
        )

    if not tracks:
        raise ParseError("No valid tracks found in playlist.")

    available_fields = {Field.NUM, Field.TITLE, Field.ARTIST}
    if has_bpm:
        available_fields.add(Field.BPM)
    if has_key:
        available_fields.add(Field.KEY)

    return ParseResult(
        tracks=tracks,
        source_kind=SourceKind.NML,
        available_fields=available_fields,
        warnings=warnings,
    )
