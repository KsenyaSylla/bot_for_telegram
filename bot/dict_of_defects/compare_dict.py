from pathlib import Path
from make_dict_of_defects import *
import importlib.util

root = Path.cwd()

def load_dict_from_py(file_path, var_name):
    spec = importlib.util.spec_from_file_location("module.name", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, var_name, {})

def compare_defect_info():
    file_path = f'{root}/bot/utils/defects_dict.py'
    prod_dict_of_defects = load_dict_from_py(file_path, "defects")
    fresh_dict_of_defects = make_dict_of_defects()
    differences = {}
    # ЭТО НЕ РАБОТАЕТ КОРРЕКТНО! поэтому надо сравнивать как-то попарно.....
    # Проверяем ключи из первого словаря
    for key, value in prod_dict_of_defects.items():
        if key not in fresh_dict_of_defects:
            differences[key] = value  # Ключ отсутствует во втором словаре
        elif fresh_dict_of_defects[key] != value:
            differences[key] = {"prod_dict_of_defects": value, "fresh_dict_of_defects": fresh_dict_of_defects[key]}  # Разные значения

    # Проверяем ключи из второго словаря, которые отсутствуют в первом
    for key, value in fresh_dict_of_defects.items():
        if key not in prod_dict_of_defects:
            differences[key] = value  # Ключ отсутствует в первом словаре

    return differences if differences else "словари равны"
print(compare_defect_info())