import openpyxl

def export_to_excel(rows, filename="result.xlsx"):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Результат"

    ws.append(["Артикул", "Наименование", "Количество"])

    for row in rows:
        ws.append(row)

    wb.save(filename)
