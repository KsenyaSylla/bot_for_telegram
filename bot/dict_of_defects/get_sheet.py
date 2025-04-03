import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from pathlib import Path

root = Path.cwd() # /home/ksylla/defects_bot
# Настройки доступа
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDS_FILE = f"{root}/dict_of_defects/credentials.json"  # Укажите путь к вашему JSON-файлу

# ID Google-таблицы (находится в URL)
SPREADSHEET_ID = "1zb3DUkAjGbdWnsLEVBGv1VNWa7pnLSxuxf-gyuHptcc"
SHEET_NAME = "Дефекты"  # Укажите название нужного листа

def download_google_sheet():
    # Авторизация
    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, SCOPE)
    gc = gspread.authorize(credentials)

    # Открываем таблицу
    sheet = gc.open_by_key(SPREADSHEET_ID)
    worksheet = sheet.worksheet(SHEET_NAME)

    # Получаем данные
    data = worksheet.get_all_records()

    # Преобразуем в DataFrame
    df = pd.DataFrame(data)
    
    return df  # Возвращаем DataFrame