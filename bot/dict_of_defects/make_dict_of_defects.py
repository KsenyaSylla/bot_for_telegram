from .get_sheet import download_google_sheet as dgs

def make_dict_of_defects():
    input_df = dgs()
    required_columns = ["Название дефекта", "Код дефекта"]
    filtered_df = input_df[required_columns]
    return filtered_df.set_index("Код дефекта")["Название дефекта"].to_dict()

def make_dict_of_statuses():
    input_df = dgs()
    required_columns = ["Код дефекта", "Статус обслуживания на роботе"]
    filtered_df = input_df[required_columns]
    #print(filtered_df.head())
    return filtered_df.set_index["Код дефекта", "Статус обслуживания на роботе"].to_dict()