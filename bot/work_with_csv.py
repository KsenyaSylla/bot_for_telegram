import pandas as pd
import json
from .utils.save_defect_history import store_defect_history
from pathlib import Path

root = Path.cwd()
db = f"{root}/bot/utils/defect_data.csv"

#ВСЕ функции возвращают сообщения для бота о случившемся обновлении либо принтуют об ошибках

def update_status(defect_value, new_status):
    new_status = str(new_status)
    try:
        df = pd.read_csv(db, dtype={'status': 'string'})
        old_status = str(get_status(defect_value))
        if old_status == new_status:
            message = f"Статус дефекта с кодом '{defect_value}' уже '{new_status}'"
            return message
        df.loc[df["defect"] == defect_value, "status"] = new_status
        try:
            df.to_csv(db, index=False)
            print("Файл сохранён успешно!")
        except Exception as e:
            print("Ошибка при сохранении:", e)

        #df.to_csv(db, index=False)
        update_history(defect_value, new_status)
        message = f"Статус дефекта с кодом '{defect_value}' изменен на '{new_status}'"
        return message
    except Exception as e:
        print(f"Ошибка обновления статуса дефекта {e}")

def update_history(defect, new_status): #история храниться в json, в python обрабатывается как словарь
    try:
        history_old = get_history(defect)#словарь
        history_for_update = store_defect_history(new_status)#словарь
        updated_history = {**history_old, **history_for_update}#скленный словарь
        updated_history_json = json.dumps(updated_history, indent=len(updated_history))#херачим json
        updated_history = str(updated_history_json)#теперь строку, чтобы не плодить ошибки
        df = pd.read_csv(db, dtype={'history': 'string'})
        df.loc[df["defect"] == defect, "history"] = updated_history
        try:
            df.to_csv(db, index=False)
            print("Файл сохранён успешно!")
        except Exception as e:
            print("Ошибка при сохранении:", e)
        #df.to_csv(db, index=False)
        message = f"Успешно обновлена история статусов дефекта с кодом '{defect}'"
        return message
    except Exception as e:
        print(f'Ошибка при обновлении истории статусов {e}')

def get_history(defect_value):
    try:
        df = pd.read_csv(db)
        row = df[df['defect'] == defect_value]
        if not row.empty:
            result = row.iloc[0]['history']#ожидаю здесь json
            if pd.isna(result) or result == '':
                result = dict()
                return result
            result = json.loads(result)#делаем из json словарь
            return result
        return dict()
        
    except Exception as e:
        print(f'Ошибка при получении истории статусов {e}')

def get_status(defect_value):    
    try:
        df = pd.read_csv(db)
        result = df[df['defect'].astype(str).str.contains(str(defect_value), na=False)]
        result = result['status'].iloc[0] if not result.empty else None
        return result
    except Exception as e:
        print(f'Ошибка при получении статуса {e}')

def show_history(defect_value):
    history = get_history(defect_value)
    if history == {}:
        message = f"История дефекта с кодом '{defect_value}' пуста"
        return message
    history = json.dumps(history, indent=len(history))
    message = f"История дефекта с кодом '{defect_value}':\n{history}"
    return message

#update_status(2258, 'on')