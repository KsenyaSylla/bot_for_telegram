from pathlib import Path
from .make_dict_of_defects import *
import importlib.util

root = Path.cwd()

def load_dict_from_py(file_path, var_name):
    spec = importlib.util.spec_from_file_location("module.name", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, var_name, {})

def compare_defect_info():
    file_path = f'{root}/utils/defects_dict.py'
    old = load_dict_from_py(file_path, "defects")
    fresh = make_dict_of_defects()
    """ old = {'1':"one", '2': "two", "3":"three", '5':'five'}#, "4":"four"
    fresh = {1:"one", 2: "two", 3:"three","4":"four"}#0:"zero",  """
    differences = {"old": [], "fresh": []}
    old = change_keys_type_to_str(old)
    fresh = change_keys_type_to_str(fresh)
    all_keys = set(old.keys()).union(set(fresh.keys()))

    for key in all_keys:
        old_value = old.get(key)
        fresh_value = fresh.get(key)

        if key not in fresh:
            # Ключ есть в old, но отсутствует в fresh
            differences["old"].append(f"{key}:{old_value}")
        elif key not in old:
            # Ключ есть в fresh, но отсутствует в old
            differences["fresh"].append(f"{key}:{fresh_value}")
        elif old_value != fresh_value:
            # Ключ есть в обоих, но значения разные
            differences["old"].append(f"{key}:{old_value}")
            differences["fresh"].append(f"{key}:{fresh_value}")
    return differences

def get_message_about_updates():
    differences = compare_defect_info()
    message = ''
    old = differences['old']
    fresh = differences['fresh']
    if len(old) == 0 and len(fresh) == 0:
        return "Изменений нет"
    if len(old) == 0:
        message = "Все значения из нынешнего словаря дефектов присутсвуют в актуальной таблице.\n"
    else:
        message = f"Измененные значения из старой версии:\n{old}\n"
    if len(fresh) == 0:
        message = f"{message}Все значения из актуальной таблицы присутствуют в нынешнем словаре.\n"
    else:   
        message = f'{message}Добавленные или измененные в актуальной таблице:\n{fresh}'
    return message

def update_dict():
    file_path = f'{root}/utils/defects_dict.py'
    old_dict = load_dict_from_py(file_path, "defects")
    old_dict = change_keys_type_to_str(old_dict)
    old_list = make_list(old_dict)
    differences = compare_defect_info()
    message = ''
    updated_list = []
    old = differences['old']
    fresh = differences['fresh']
    if len(old) == 0 and len(fresh) == 0:
        return "Апдейт не требуется"
    if not len(old) == 0:
        #нужно из old_list удалить значения, которые содержаться в old
        updated_list = updated_list.append([item for item in old_list if item not in set(old)])
        message = f'Из старой версии удалены значения\n{old}\n'
    if not len(fresh) == 0:
        #нужно в оld_list доавить значения из fresh
        updated_list = updated_list.append(fresh)
        message = f"{message}В словарь добавлены значения\n{fresh}\n"
    # Открываем файл в режиме записи ("w"), чтобы удалить старые данные
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(f"defects = {updated_list}\n")
    return message

def change_keys_type_to_str(data):
    string_keys_dict = {str(key): value for key, value in data.items()}
    return string_keys_dict

def make_list(dict_of_def):
    list_of_def = [f"{key}:{value}" for key, value in dict_of_def.items()]
    return list_of_def

def make_dict(list_of_def):
    dict_of_def = {item.split(':')[0]: item.split(':')[1] for item in list_of_def}
    return dict_of_def

""" print(get_message_about_updates())
print(update_dict()) """