import pytest

from traktor_export.models import Field, SourceKind
from traktor_export.parsers.errors import ParseError
from traktor_export.parsers.html_parser import parse_html_playlist


def test_parses_all_tracks(html_playlist_path):
    result = parse_html_playlist(html_playlist_path)
    assert result.source_kind == SourceKind.HTML
    assert len(result.tracks) == 13


def test_available_fields(html_playlist_path):
    result = parse_html_playlist(html_playlist_path)
    assert result.available_fields == {Field.NUM, Field.TITLE, Field.ARTIST, Field.LABEL}


def test_first_track_fields(html_playlist_path):
    result = parse_html_playlist(html_playlist_path)
    first = result.tracks[0]
    assert first.num == 1
    assert first.artist == "Ginchy"
    assert first.label == "SPRS"
    # "[Extended Mix]" must be stripped from the title
    assert "Extended" not in first.title
    assert first.title == "Uninvited (feat. Yasmin Jane)"


def test_malformed_html_raises(tmp_path):
    bad_file = tmp_path / "bad.html"
    bad_file.write_text("<html><body>not a playlist</body></html>")
    with pytest.raises(ParseError):
        parse_html_playlist(str(bad_file))
