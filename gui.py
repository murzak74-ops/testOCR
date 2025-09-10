import streamlit as st
import pandas as pd
from exporter import export_to_excel
from ocr_utils import process_files
from parser import parse_text
import tempfile
import os

st.title("📄 OCR-приложение для товаров")

uploaded_files = st.file_uploader(
    "Загрузите PDF или изображения (можно несколько файлов)",
    type=["pdf", "jpg", "jpeg", "png"],
    accept_multiple_files=True
)

if uploaded_files:
    all_rows = []
    raw_texts = []

    for file in uploaded_files:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(file.read())
            tmp_path = tmp.name

        text = process_files(tmp_path)
        raw_texts.append((file.name, text))
        rows = parse_text(text)
        all_rows.extend(rows)

        os.remove(tmp_path)

    # Показываем сырое распознанное содержимое
    with st.expander("🔍 Распознанный текст"):
        for fname, text in raw_texts:
            st.subheader(fname)
            st.text_area("Текст", text, height=200)

    # Показываем предварительный разбор по строкам
    with st.expander("📑 Предварительная сегментация строк"):
        for row in all_rows:
            st.write(row)

    if all_rows:
        df = pd.DataFrame(all_rows, columns=["Артикул", "Наименование", "Количество"])
        st.success("✅ Данные распознаны")
        st.dataframe(df)

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
