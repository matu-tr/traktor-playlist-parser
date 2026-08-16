from pathlib import Path

import pytest

FIXTURES = Path(__file__).parent.parent


@pytest.fixture
def html_playlist_path() -> str:
    return str(FIXTURES / "wats04.html")


@pytest.fixture
def nml_playlist_path() -> str:
    return str(FIXTURES / "wats04.nml")
