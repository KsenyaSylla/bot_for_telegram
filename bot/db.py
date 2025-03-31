import psycopg2
import json
from utils.save_defect_history import store_defect_history
from utils.defects_dict import defects
from utils.check_defect import *
from config import DB_CONFIG

def update_status(defect_value, new_status):
    """Обновляет значение status в таблице defects_status по значению defect."""
    defect_value = get_defect_code(defect_value)# запрос к питонячьему словарю
    #если статус новый совпадает со старым, то нужно об этом оповесстить и не обновлять ничего!
    new_status = str(new_status)
    if defect_value == "Дефект не найден":
        return defect_value
    old_status = str(get_status(defect_value))
    if old_status == new_status:
        message = f"Статус дефекта с кодом '{defect_value}' уже '{new_status}'"
        return message
    try:
        history = get_updated_history(defect_value, new_status)
    except:
        print(f'Ошибка при получении обновленной истории: {e}')
    try:
        # Подключение к БД
        conn = connect_db()
        cursor = conn.cursor()
        # SQL-запрос для обновления
        query = """
        UPDATE defects_status
        SET status = %s,
        history = %s
        WHERE defect = %s;
        """
        
        # Выполнение запроса
        cursor.execute(query, (new_status, history, defect_value))
        conn.commit()

        message_updated = f"Запись обновлена: defect={defect_value} -> status={new_status}"
        return message_updated

    except psycopg2.Error as e:
        print(f"Ошибка при обновлении БД: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_updated_history(defect, new_status): #история храниться в json, в python обрабатывается как словарь
    history_old = get_history(defect)
    history_for_update = store_defect_history(new_status)
    updated_history = {**history_old, **history_for_update}#скленный словарь
    updated_history_json = json.dumps(updated_history, indent=len(updated_history))#херачим json
    updated_history = str(updated_history_json)#теперь строку, чтобы не плодить ошибки
    return updated_history

def get_history(defect_value):
    try:
        conn = connect_db()
        cursor = conn.cursor()

        # Безопасный SQL-запрос с параметром
        query = "SELECT history FROM your_table WHERE defect = ?"
        cursor.execute(query, (defect_value,))

        results = cursor.fetchall()

        for row in results:
            history_data = json.loads(row[0])  # Преобразуем строку JSON в объект Python, скорее всего словарь
        return history_data

    except Exception as e:
        print("Ошибка при получении истории:", e)

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

#show_history(message.text)

def connect_db():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.Error as e:
        print(f"Ошибка подключения: {e}")

def get_status(defect_value):
    defect_value = get_defect_code(defect_value)
    try:
        conn = connect_db()
        cursor = conn.cursor()

        # Безопасный SQL-запрос с параметром
        query = "SELECT status FROM your_table WHERE defect = ?"
        cursor.execute(query, (defect_value,))

        result = cursor.fetchone()
        status = str(result[0])
        return status

    except Exception as e:
        print("Ошибка при получении статуса:", e)

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

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

"""
def process_defect(resieved_str, action):
    try:
        defect = get_defect(resieved_str)
        if defect == "Несуществующий код дефекта" or defect == "Несуществующее название дефекта":
            return defect #возвращаем в бота сообщение об ошибке
        else:
            if action == 'on' or action == 'off':
                message = update_status(defect, action)
            elif action == 'history':
                message = str(get_history(defect)) #приходит словарь, нужно сделать красоту, чтобы возвращалось что-то дельное. Для начала в строку
            else:
                message = str(get_status(defect)) #по умолчанию приходит строка, на всякий случай приведем к строковому значению
        return message
    except Exception as e:
        print(f'Ошибка при получении данных по дефекту: {e}')
def get_defect(defect):
    defect = str(defect)#на всякий случай приведем к строке, чтобы точно было то, что нам нужно
    try:
        if len(defect)>7:
            for key, value in defects.items():
                if defect.lower() in value.lower():
                    return key
            return "Несуществующее название дефекта"
            
        else:
            for key, value in defects.items():
                if defect.lower() in key.lower():
                    return key
            return "Несуществующий код дефекта"
    
    except Exception as e:
        print(f'Ошибка при обработке дефекта: {e}')
"""