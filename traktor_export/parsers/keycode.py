# Traktor's MUSICAL_KEY VALUE is a 0-23 enum: 0-11 are the majors in chromatic
# order starting at C, 12-23 are the relative minors in the same order.
TRAKTOR_KEY_NAMES: dict[int, tuple[str, str]] = {
    0: ("8B", "C maj"),
    1: ("3B", "Db maj"),
    2: ("10B", "D maj"),
    3: ("5B", "Eb maj"),
    4: ("12B", "E maj"),
    5: ("7B", "F maj"),
    6: ("2B", "Gb maj"),
    7: ("9B", "G maj"),
    8: ("4B", "Ab maj"),
    9: ("11B", "A maj"),
    10: ("6B", "Bb maj"),
    11: ("1B", "B maj"),
    12: ("5A", "C min"),
    13: ("12A", "Db min"),
    14: ("7A", "D min"),
    15: ("2A", "Eb min"),
    16: ("9A", "E min"),
    17: ("4A", "F min"),
    18: ("11A", "Gb min"),
    19: ("6A", "G min"),
    20: ("1A", "Ab min"),
    21: ("8A", "A min"),
    22: ("3A", "Bb min"),
    23: ("10A", "B min"),
}


def key_code_to_name(value: int | None, style: str = "combined") -> str:
    if value is None or value not in TRAKTOR_KEY_NAMES:
        return f"Unknown({value})"
    camelot, standard = TRAKTOR_KEY_NAMES[value]
    if style == "camelot":
        return camelot
    if style == "standard":
        return standard
    return f"{camelot} - {standard}"
