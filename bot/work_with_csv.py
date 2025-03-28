import pandas as pd
import json
from .utils.save_defect_history import store_defect_history
from .utils.check_defect import *
from pathlib import Path

root = Path.cwd()
db = f"{root}/bot/utils/defect_data.csv"

#ВСЕ функции возвращают сообщения для бота о случившемся обновлении либо принтуют об ошибках

def update_status(defect_value, new_status):
    new_status = str(new_status)
    defect_value = get_defect_code(defect_value)
    if defect_value == "Дефект не найден":
        return defect_value
    df = pd.read_csv(db, dtype={'status': 'string'})
    old_status = str(get_status(defect_value))
    if old_status == new_status:
        message = f"Статус дефекта с кодом '{defect_value}' уже '{new_status}'"
        return message
    df.loc[df["defect"] == defect_value, "status"] = new_status
    try:
        df.to_csv(db, index=False, encoding='utf-8')
    except Exception as e:
        print("Ошибка при сохранении:", e)

    #df.to_csv(db, index=False)
    update_history(defect_value, new_status)
    message = f"Статус дефекта с кодом '{defect_value}' изменен на '{new_status}'"
    return message


def update_history(defect, new_status): #история храниться в json, в python обрабатывается как словарь
    defect_code = get_defect_code(defect)
    history_old = get_history(defect_code)#словарь
    history_for_update = store_defect_history(new_status)#словарь
    updated_history = {**history_old, **history_for_update}#скленный словарь
    updated_history_json = json.dumps(updated_history, indent=len(updated_history))#херачим json
    updated_history = str(updated_history_json)#теперь строку, чтобы не плодить ошибки
    df = pd.read_csv(db, dtype={'history': 'string'})
    df.loc[df["defect"] == defect_code, "history"] = updated_history
    try:
        df.to_csv(db, index=False, encoding='utf-8')
    except Exception as e:
        print("Ошибка при сохранении:", e)
    #df.to_csv(db, index=False)
    message = f"Успешно обновлена история статусов дефекта '{defect}'"
    return message

def get_history(defect_value):
    defect_value = get_defect_code(defect_value)
    if defect_value == "Дефект не найден":
        return defect_value
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
        

def get_status(defect_value):    
    defect_value = get_defect_code(defect_value)
    if defect_value == "Дефект не найден":
        return defect_value
    df = pd.read_csv(db)
    result = df[df['defect'].astype(str).str.contains(str(defect_value), na=False)]
    result = str(result['status'].iloc[0])
    return result

def show_history(defect_value):
    defect_value = get_defect_code(defect_value)
    if defect_value == "Дефект не найден":
        return defect_value
    history = get_history(defect_value)
    if history == {}:
        message = f"История дефекта '{defect_value}' пуста"
        return message
    history = json.dumps(history, indent=len(history))
    message = f"История дефекта '{defect_value}':\n{history}"
    return message

def get_defect_info(defect):
    defect_code = get_defect_code(defect)
    if is_number(defect):
        defect_name = get_defect_name(defect)
        message = f"Название дефекта с кодом {defect}\n{defect_name}"
        return message
    elif defect_code == "Дефект не найден":
        message = defect_code
        return message
    message = f'Дефект "{defect}"\nкод = {defect_code}'
    return message

#print(get_status(2258))
#update_status('2258', 'on')