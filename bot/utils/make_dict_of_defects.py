import csv
from pathlib import Path

root = Path.cwd()
#это свежие файлы, которые должны быть актуальны
input_file = f"{root}/data/Робот_Опти - Дефекты.csv"
output_file = f"{root}/data/defects_saved.csv"
#это предыдущая версия, с которой будем сравнивать и обновлять пр необходимости
output_file = f"{root}/test/defects_saved.csv"
#а это рабочий файл, который используется в боте
defect_dict_file = f'{root}/data/defects_dict.py'

def make_dict_of_defects(input_file):
    defects_dict = {}
    with open(input_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            defects_dict[row["Код дефекта"]] = row["Название дефекта"]

    with open(output_file, mode="w", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Код дефекта", "Название дефекта"])
        for code, name in defects_dict.items():
            writer.writerow([code, name])

    with open(defect_dict_file, "w", encoding="utf-8") as file:
        file.write(f"defects = {defects_dict}")

make_dict_of_defects(input_file)

# написать еще функцию сравнения нашего словаря со свежесобранными, чтобы пары код-название были актуальными (позже) для этот есть смысл посылать запрос в гугл-таблицы, скачивать оттуда файлик в нужный каталогк в формате csv, выуживать из него нужную инфу,  а потом сравнивать получившийся файл с тем, лежит у нас, и из которого формируется словарь. Если есть отлилчия - переписываем словарь, если нет- то на нет и суда нет.
"""
Ответ GPT по поводу выгрузки файла с гугл доков
Использование API Google Sheets
Этот метод работает даже с закрытыми таблицами, но требует API-ключа.

📌 Шаги:
Включить API Google Sheets в Google Cloud Console
Создать сервисный аккаунт, скачать credentials.json
Подключить gspread и pandas
📝 Установка зависимостей
bash
Копировать
pip install gspread pandas
📝 Код с API
python
Копировать
import gspread
import pandas as pd

# Авторизация через сервисный аккаунт
gc = gspread.service_account(filename="credentials.json")

# Открытие таблицы
SHEET_NAME = "Название вашей таблицы"
sh = gc.open(SHEET_NAME)

# Открываем первый лист
worksheet = sh.sheet1

# Получаем данные
data = worksheet.get_all_records()

# Конвертируем в CSV
df = pd.DataFrame(data)
df.to_csv("table.csv", index=False, encoding="utf-8")

print("Файл сохранен как table.csv")
"""