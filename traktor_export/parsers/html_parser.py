import re

from bs4 import BeautifulSoup

from ..models import Field, ParseResult, SourceKind, Track
from ..text_utils import remove_extended_mix
from .errors import ParseError


def normalize_html_text(raw_text: str) -> str:
    """Strip NUL bytes. Pure in-memory transform, never touches disk."""
    return re.sub('\x00', '', raw_text)


def parse_html_playlist(path: str) -> ParseResult:
    with open(path, encoding="utf8", errors="replace") as f:
        raw = f.read()
    html = normalize_html_text(raw)

    soup = BeautifulSoup(html, "html.parser")
    rows = soup.select("table.border tr")[1:]
    if not rows:
        raise ParseError(
            "No track rows found — is this a Traktor 'Track List' HTML export?"
        )

    tracks: list[Track] = []
    for i, row in enumerate(rows, start=1):
        cells = row.select("td")
        if len(cells) != 4:
            raise ParseError(f"Row {i}: expected 4 columns, found {len(cells)}.")
        num_cell, title_cell, artist_cell, label_cell = cells
        num_text = num_cell.get_text().strip()
        tracks.append(
            Track(
                num=int(num_text) if num_text.isdigit() else i,
                title=remove_extended_mix(title_cell.get_text().strip()),
                artist=artist_cell.get_text().strip(),
                label=label_cell.get_text().strip(),
            )
        )

    return ParseResult(
        tracks=tracks,
        source_kind=SourceKind.HTML,
        available_fields={Field.NUM, Field.TITLE, Field.ARTIST, Field.LABEL},
    )
