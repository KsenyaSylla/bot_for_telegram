import pandas as pd
import json
from utils.save_defect_history import store_defect_history
from pathlib import Path

root = Path.cwd()
db = f"{root}/bot/utils/defect_data.csv"

#ВСЕ функции возвращают сообщения для бота о случившемся обновлении либо принтуют об ошибках

def update_status(defect_value, new_status):
    df = pd.read_csv(db)
    try:
        df.loc[df["defect"] == defect_value, "status"] = new_status
        update_history(defect_value, new_status)
        message = f"Статус дефекта с кодом '{defect_value}' изменен на '{new_status}'"
        return message
    except Exception as e:
        print(f"Ошибка обновления статуса дефекта {e}")

def update_history(defect, new_status): #история храниться в json, в python обрабатывается как словарь
    df = pd.read_csv(db)
    try:
        history_old, message = get_history(defect)
        history_for_update = store_defect_history(new_status)#словарь
        updated_history = {**history_old, **history_for_update}#скленный словарь
        updated_history_json = json.dump(updated_history, indent=len(updated_history))#херачим json
        df.loc[df["defect"] == defect, "history"] = updated_history_json
        message = f"Успешно обновлена история статусов дефекта с кодом '{defect}'"
        return message
    except Exception as e:
        print(f'Ошибка при обновлении истории статусов {e}')

def get_history(defect_value):
    df = pd.read_csv(db)
    try:
        results = df[df['defect'].astype(str).str.contains(str(defect_value), na=False)]
        results = results['history'].iloc[0] if not results.empty else None #это дб json строка
        message = f"История дефекта с кодом '{defect_value}':\n {results}"
        results = json.loads(results)
        return results, message    
    except Exception as e:
        print(f'Ошибка при получении истории статусов {e}')

def get_status(defect_value):
    df = pd.read_csv(db)
    try:
        result = df[df['defect'].astype(str).str.contains(str(defect_value), na=False)]
        result = result['status'].iloc[0] if not result.empty else None
        message = f'{defect_value}: {result}'
        return message
    except Exception as e:
        print(f'Ошибка при получении статуса {e}')

