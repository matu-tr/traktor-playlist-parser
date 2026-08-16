import pytest

from traktor_export.formatters import FormatError, format_output
from traktor_export.models import Field, FormatStyle, Track

TRACKS = [
    Track(num=1, title="Title A", artist="Artist A", label="Label A", bpm=124.0, key="7A - D min"),
    Track(num=2, title="Title B", artist="Artist B", label="Label B"),
]
ALL_FIELDS = [Field.NUM, Field.TITLE, Field.ARTIST, Field.LABEL, Field.BPM, Field.KEY]
CORE_FIELDS = [Field.TITLE, Field.ARTIST]


def test_numbered_list_with_all_fields():
    text = format_output(TRACKS, ALL_FIELDS, FormatStyle.NUMBERED_LIST)
    assert text.splitlines() == [
        "1. Artist A - Title A [Label A] 124 BPM 7A - D min",
        "2. Artist B - Title B [Label B]",
    ]


def test_numbered_list_core_fields_only():
    text = format_output(TRACKS, CORE_FIELDS, FormatStyle.NUMBERED_LIST)
    assert text.splitlines() == ["Artist A - Title A", "Artist B - Title B"]


def test_cue_sheet_has_intro_header():
    text = format_output(TRACKS, ALL_FIELDS, FormatStyle.CUE_SHEET)
    lines = text.splitlines()
    assert lines[0] == "00:00 Intro"
    assert lines[1] == "00:00 Artist A - Title A [Label A] 124 BPM 7A - D min"


def test_stanza_block_separates_tracks_with_blank_line():
    text = format_output(TRACKS, ALL_FIELDS, FormatStyle.STANZA_BLOCK)
    blocks = text.split("\n\n")
    assert len(blocks) == 2
    assert blocks[0].splitlines() == ["Title A", "Artist A", "[Label A]", "124 BPM", "7A - D min"]


def test_custom_template():
    text = format_output(
        TRACKS, [], FormatStyle.CUSTOM, "{track_number}. {artist} - {title} [{label}]"
    )
    assert text.splitlines() == [
        "1. Artist A - Title A [Label A]",
        "2. Artist B - Title B [Label B]",
    ]


def test_custom_template_unknown_placeholder_raises():
    with pytest.raises(FormatError):
        format_output(TRACKS, [], FormatStyle.CUSTOM, "{nonexistent}")


def test_custom_template_missing_optional_value_is_blank():
    tracks = [Track(num=1, title="T", artist="A")]
    text = format_output(tracks, [], FormatStyle.CUSTOM, "{artist} - {title} [{label}] {bpm} {key}")
    assert text == "A - T []  "
