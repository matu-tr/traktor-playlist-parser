# Traktor Playlist Converter

A small desktop app that turns a Traktor playlist export into a plain-text
tracklist. Drag a file onto the window, pick the fields and format you want,
and save the result.

## Features

- **Drag and drop** either a Traktor HTML "Track List" export (`.html`) or a
  native Traktor collection file (`.nml`) — the latter also exposes BPM and
  musical key (Camelot notation).
- **Pick your fields**: track number, title, artist, label, BPM, key.
- **Built-in formats**: numbered list, cue sheet (`00:00` timestamps), or a
  stanza block.
- **Custom format**: write your own template, e.g.
  `{track_number}. {artist} - {title} [{label}]`, using placeholders for any
  available field.

## Download

Prebuilt macOS and Windows apps are published on the
[Releases](https://github.com/matu-tr/traktor-playlist-parser/releases) page.

## Running from source

```bash
pip install -e .
python main.py
```

This launches the GUI. Requires Python 3.11+.

## Command line

The same conversion is also available without the GUI:

```bash
python main.py path/to/playlist.html --format list -o tracklist.txt
python main.py path/to/playlist.nml --format custom \
  --template "{track_number}. {artist} - {title} [{label}]"
```

`--format` accepts `list`, `cue`, `stanza`, or `custom` (paired with
`--template`).

## Development

```bash
pip install -e ".[dev]"
pytest
ruff check .
```

## License

MIT — see [LICENSE](LICENSE).

This project uses [PySide6](https://pypi.org/project/PySide6/), which is
licensed under LGPLv3.
