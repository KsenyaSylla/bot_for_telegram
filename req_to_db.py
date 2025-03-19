import psycopg2
import json
from utils.save_defect_history import store_defect_history
from config import DB_CONFIG
# Параметры подключения к базе данных

#интересно, можно ли как-то сократить количество запросов в бд с обновлением истории дефектов

def update_status(defect_value, new_status):
    """Обновляет значение status в таблице defects_status по значению defect."""
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
    updated_history = json.dump({**history_old, **history_for_update})
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

def connect_db():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.Error as e:
        print(f"Ошибка подключения: {e}")

def get_status(defect_value):
    try:
        conn = connect_db()
        cursor = conn.cursor()

        # Безопасный SQL-запрос с параметром
        query = "SELECT status FROM your_table WHERE defect = ?"
        cursor.execute(query, (defect_value,))

        result = cursor.fetchone()
        status = result[0]
        return status

    except Exception as e:
        print("Ошибка при получении статуса:", e)

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



