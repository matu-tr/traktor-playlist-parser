import argparse
from pathlib import Path

from traktor_export.formatters import DEFAULT_CUSTOM_TEMPLATE, format_output
from traktor_export.models import FormatStyle
from traktor_export.parsers.html_parser import parse_html_playlist
from traktor_export.parsers.nml_parser import parse_nml_playlist

_STYLE_MAP = {
    "list": FormatStyle.NUMBERED_LIST,
    "cue": FormatStyle.CUE_SHEET,
    "stanza": FormatStyle.STANZA_BLOCK,
    "custom": FormatStyle.CUSTOM,
}


def main():
    parser = argparse.ArgumentParser(description="Traktor playlist converter")
    parser.add_argument("input", nargs="?", help="Path to .html/.nml (omit to launch GUI)")
    parser.add_argument("-o", "--output", help="Output file (defaults to stdout)")
    parser.add_argument("--format", choices=list(_STYLE_MAP), default="list")
    parser.add_argument(
        "--template",
        default=DEFAULT_CUSTOM_TEMPLATE,
        help="Template for --format custom, e.g. '{track_number}. {artist} - {title} [{label}]'",
    )
    args = parser.parse_args()

    if not args.input:
        from traktor_export.gui.app import main as run_gui

        run_gui()
        return

    ext = Path(args.input).suffix.lower()
    if ext in (".html", ".htm"):
        result = parse_html_playlist(args.input)
    elif ext == ".nml":
        result = parse_nml_playlist(args.input)
    else:
        raise SystemExit(f"Unsupported file type: {ext or '(none)'}")

    text = format_output(
        result.tracks, list(result.available_fields), _STYLE_MAP[args.format], args.template
    )

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text)
    else:
        print(text)


if __name__ == "__main__":
    main()
