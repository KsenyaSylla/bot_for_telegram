import gspread
import os
import json
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from dotenv import load_dotenv
load_dotenv()


# Настройки доступа
CREDS_DICT = json.dumps({
    "type": os.getenv("TYPE"),
    "project_id": os.getenv("PROJECT_ID"),
    "private_key_id": os.getenv("PRIVATE_KEY_ID"),
    "private_key": os.getenv("PRIVATE_KEY"),
    "client_email": os.getenv("CLIENT_EMAIL"),
    "client_id": os.getenv("CLIENT_ID"),
    "auth_uri": os.getenv("AUTH_URI"),
    "token_uri": os.getenv("TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL"),
    "universe_domain": os.getenv("UNIVERSE_DOMAIN")
})
CREDS_DICT = json.loads(CREDS_DICT)
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]


# ID Google-таблицы (находится в URL)
SPREADSHEET_ID = "1zb3DUkAjGbdWnsLEVBGv1VNWa7pnLSxuxf-gyuHptcc"
SHEET_NAME = "Дефекты"  # Укажите название нужного листа

def download_google_sheet():
    # Авторизация
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(CREDS_DICT, SCOPE)
    gc = gspread.authorize(credentials)

    # Открываем таблицу
    sheet = gc.open_by_key(SPREADSHEET_ID)
    worksheet = sheet.worksheet(SHEET_NAME)

    # Получаем данные
    data = worksheet.get_all_records()

    # Преобразуем в DataFrame
    df = pd.DataFrame(data)
    
    return df  # Возвращаем DataFrame

print(download_google_sheet().head())