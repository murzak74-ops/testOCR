import re

def parse_text(text: str):
    rows = []

    # Разделяем текст на кандидатов: по переводам строк и по "шт"
    candidates = re.split(r"(?:\n|шт[.,]?\s)", text, flags=re.IGNORECASE)

    for c in candidates:
        line = c.strip()
        if not line:
            continue

        parts = line.split()

        # Ищем количество в конце (число)
        qty = ""
        if parts and re.match(r"^\d+$", parts[-1]):
            qty = parts[-1]
            parts = parts[:-1]

        # Ищем артикул (первое «похожее на код» слово: буквы+цифры)
        article = ""
        if parts and re.match(r"^[A-ZА-Я0-9-]+$", parts[0], flags=re.IGNORECASE):
            article = parts[0]
            parts = parts[1:]

        # Остальное считаем наименованием
        name = " ".join(parts)

        if article or name or qty:
            rows.append([article, name.strip(), qty])

    return rows
