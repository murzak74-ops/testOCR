import re

def parse_text(text: str):
    rows = []
    lines = text.split("\n")
    pattern = re.compile(r"(\w+)\s+([\w\s]+)\s+(\d+)")
    for line in lines:
        match = pattern.match(line.strip())
        if match:
            article, name, qty = match.groups()
            rows.append([article, name.strip(), qty])
    return rows
