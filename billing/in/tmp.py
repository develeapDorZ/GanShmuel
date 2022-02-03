import openpyxl

wb_obj = openpyxl.load_workbook("rates.xlsx")
sheet = wb_obj.active
sheet = sheet.iter_rows(min_row=0)
print(sheet)

for row in sheet:
    print(f'{row[0].value} {row[1].value} {row[2].value}')