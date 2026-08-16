import re


def remove_extended_mix(title: str) -> str:
    pattern = re.compile(r'\[Extended\s+(.*?Mix)\]|\(Extended\s+(.*?Mix)\)', re.IGNORECASE)

    def replace_pattern(match):
        bracket_type = '[' if match.group(0).startswith('[') else '('
        mix_part = match.group(1) or match.group(2)
        if 'Mix' == mix_part.strip():
            return ''
        return f'{bracket_type}{mix_part}{bracket_type.replace("[", "]").replace("(", ")")}'

    title = re.sub(pattern, replace_pattern, title).strip()
    title = re.sub(r'\s+-\s+', ' - ', title)
    title = re.sub(r'\[Extended Mix\]|\(Extended Mix\)', '', title, flags=re.IGNORECASE).strip()
    return title
