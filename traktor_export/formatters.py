import string

from .models import Field, FormatStyle, Track

CUSTOM_TEMPLATE_PLACEHOLDERS = ["track_number", "num", "artist", "title", "label", "bpm", "key"]
DEFAULT_CUSTOM_TEMPLATE = "{track_number}. {artist} - {title} [{label}]"


class FormatError(Exception):
    pass


def _core(t: Track, fields: list[Field]) -> str:
    parts = []
    if Field.ARTIST in fields:
        parts.append(t.artist)
    if Field.TITLE in fields:
        parts.append(t.title)
    return " - ".join(parts)


def _extras(t: Track, fields: list[Field]) -> str:
    extras = []
    if Field.LABEL in fields and t.label:
        extras.append(f"[{t.label}]")
    if Field.BPM in fields and t.bpm is not None:
        extras.append(f"{t.bpm:.0f} BPM")
    if Field.KEY in fields and t.key:
        extras.append(t.key)
    return f" {' '.join(extras)}" if extras else ""


def format_numbered_list(tracks: list[Track], fields: list[Field]) -> str:
    lines = []
    for t in tracks:
        prefix = f"{t.num}. " if Field.NUM in fields else ""
        lines.append(f"{prefix}{_core(t, fields)}{_extras(t, fields)}")
    return "\n".join(lines)


def format_cue_sheet(tracks: list[Track], fields: list[Field]) -> str:
    lines = ["00:00 Intro"]
    for t in tracks:
        lines.append(f"00:00 {_core(t, fields)}{_extras(t, fields)}")
    return "\n".join(lines)


def format_stanza_block(tracks: list[Track], fields: list[Field]) -> str:
    blocks = []
    for t in tracks:
        lines = []
        if Field.TITLE in fields:
            lines.append(t.title)
        if Field.ARTIST in fields:
            lines.append(t.artist)
        if Field.LABEL in fields and t.label:
            lines.append(f"[{t.label}]")
        if Field.BPM in fields and t.bpm is not None:
            lines.append(f"{t.bpm:.0f} BPM")
        if Field.KEY in fields and t.key:
            lines.append(t.key)
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks)


def _track_placeholders(t: Track) -> dict:
    return {
        "track_number": t.num,
        "num": t.num,
        "title": t.title,
        "artist": t.artist,
        "label": t.label or "",
        "bpm": f"{t.bpm:.0f}" if t.bpm is not None else "",
        "key": t.key or "",
    }


def validate_custom_template(template: str) -> None:
    """Raise FormatError if the template references an unknown placeholder
    or is otherwise malformed. Cheap upfront check so the GUI can reject
    a bad template before the user picks a save path."""
    try:
        fields_used = [name for _, name, _, _ in string.Formatter().parse(template) if name]
    except ValueError as exc:
        raise FormatError(f"Invalid format template: {exc}") from exc
    unknown = [f for f in fields_used if f not in CUSTOM_TEMPLATE_PLACEHOLDERS]
    if unknown:
        raise FormatError(f"Unknown field(s): {', '.join(unknown)}")


def format_custom(tracks: list[Track], template: str) -> str:
    validate_custom_template(template)
    lines = []
    for t in tracks:
        try:
            lines.append(template.format(**_track_placeholders(t)))
        except (KeyError, IndexError, ValueError) as exc:
            raise FormatError(f"Could not apply format template: {exc}") from exc
    return "\n".join(lines)


_FORMATTERS = {
    FormatStyle.NUMBERED_LIST: format_numbered_list,
    FormatStyle.CUE_SHEET: format_cue_sheet,
    FormatStyle.STANZA_BLOCK: format_stanza_block,
}


def format_output(
    tracks: list[Track], fields: list[Field], style: FormatStyle, template: str | None = None
) -> str:
    if style == FormatStyle.CUSTOM:
        return format_custom(tracks, template or DEFAULT_CUSTOM_TEMPLATE)
    return _FORMATTERS[style](tracks, fields)
