from data.defects_dict import defects
from req_to_db import *

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
                #import json
                #d = {"name": "Alice", "age": 25}
                #s = json.dumps(d)  
                #print(s)  # '{"name": "Alice", "age": 25}'
            else:
                message = str(get_status(defect)) #по умолчанию приходит строка, на всякий случай приведем к строковому значению
        return message
    except Exception as e:
        print(f'Ошибка при получении данных по дефекту: {e}')


print(process_defect('Течь сифона'))
