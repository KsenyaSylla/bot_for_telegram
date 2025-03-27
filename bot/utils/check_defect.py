from .defects_dict import defects

def get_defect_code(defect_value):# возвращать число - код дефекта
    try:
        if is_number(defect_value):
            defect_code =  int(defect_value)
            return defect_code
        defect_value = defect_value.lower()
        for code in defects:
            defect = defects[code].lower()
            if defect == defect_value:
                return int(code)
        return "Дефект не найден"
    except Exception as e:
        print(f'Поиск в словаре. Ошибка: {e}')


def get_defect_name(defect_code):
    try:
        for code in defects:
            if code == defect_code:
                return str(defects[code])
        return "Дефект не найден"
    except Exception as e:
        print(f'Поиск в словаре. Ошибка: {e}')

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

#print(check_defect("Наклонившееся дерево, ветка"))