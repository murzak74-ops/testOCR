import pytesseract
from pdf2image import convert_from_path
from PIL import Image

def process_files(filepath: str) -> str:
    text = ""
    if filepath.lower().endswith(".pdf"):
        images = convert_from_path(filepath)
        for img in images:
            text += pytesseract.image_to_string(img, lang="rus") + "\n"
    else:
        img = Image.open(filepath)
        text = pytesseract.image_to_string(img, lang="rus")
    return clean_text(text)

def clean_text(text: str) -> str:
    # Простая очистка
    replacements = {
        "\n": " ",
        "  ": " ",
        "0": "О",
        "1": "I",
        "5": "S"
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text
