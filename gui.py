import streamlit as st
import pandas as pd
from exporter import export_to_excel
from ocr_utils import process_files
from parser import parse_text
import tempfile
import os

st.title("📄 OCR-приложение для товаров")

# Загрузка файлов
uploaded_files = st.file_uploader(
    "Загрузите PDF или изображения (можно несколько файлов)",
    type=["pdf", "jpg", "jpeg", "png"],
    accept_multiple_files=True
)

if uploaded_files:
    all_rows = []

    for file in uploaded_files:
        # Сохраняем временный файл для OCR
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(file.read())
            tmp_path = tmp.name

        text = process_files(tmp_path)
        rows = parse_text(text)
        all_rows.extend(rows)

        os.remove(tmp_path)  # удаляем временный файл

    if all_rows:
        df = pd.DataFrame(all_rows, columns=["Артикул", "Наименование", "Количество"])
        st.success("✅ Данные распознаны")
        st.dataframe(df)

        # Экспорт в Excel
        export_to_excel(all_rows, "result.xlsx")
        with open("result.xlsx", "rb") as f:
            st.download_button(
                "📥 Скачать result.xlsx",
                f,
                file_name="result.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    else:
        st.warning("⚠️ Не удалось извлечь данные")
