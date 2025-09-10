import re

def parse_text(text: str):
    rows = []
    lines = text.splitlines()

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Разделяем по табам или 2+ пробелам
        parts = re.split(r"\s{2,}|\t", line)

        if len(parts) >= 3:
            article = parts[0]
            qty = parts[-1] if parts[-1].isdigit() else ""
            name = " ".join(parts[1:-1]) if qty else " ".join(parts[1:])
            rows.append([article, name.strip(), qty])
        elif len(parts) == 2:
            # Например: "12345   Товар без количества"
            rows.append([parts[0], parts[1], ""])
        else:
            # Сохраняем хотя бы строку как «Наименование»
            rows.append(["", line, ""])

    return rows
