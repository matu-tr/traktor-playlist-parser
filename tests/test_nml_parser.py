import pytest

from traktor_export.models import Field, SourceKind
from traktor_export.parsers.nml_parser import list_playlist_names, parse_nml_playlist


def test_lists_playlist_names(nml_playlist_path):
    assert list_playlist_names(nml_playlist_path) == ["wats04"]


def test_parses_all_tracks_in_playlist_order(nml_playlist_path):
    result = parse_nml_playlist(nml_playlist_path)
    assert result.source_kind == SourceKind.NML
    assert len(result.tracks) == 13
    assert result.tracks[0].artist == "Ginchy"
    assert result.tracks[0].num == 1


def test_bpm_and_key_available_no_label(nml_playlist_path):
    result = parse_nml_playlist(nml_playlist_path)
    assert Field.BPM in result.available_fields
    assert Field.KEY in result.available_fields
    assert Field.LABEL not in result.available_fields
    assert all(t.label is None for t in result.tracks)


def test_key_code_converted_to_camelot_notation(nml_playlist_path):
    result = parse_nml_playlist(nml_playlist_path)
    first = result.tracks[0]
    # MUSICAL_KEY VALUE="14" in the fixture -> 7A / D min
    assert first.key == "7A - D min"
    assert first.bpm == pytest.approx(124.0, abs=0.5)
