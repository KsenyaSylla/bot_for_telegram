from datetime import datetime

def take_date():
    month = {
        '01' : "Jan",
        '02' : "Feb",
        '03' : "Mar",
        '04' : "Apr",
        '05' : "May",
        '06' : "Jun",
        '07' : "Jul",
        '08' : "Avg",
        '09' : "Sep",
        '10' : "Okt",
        '11' : "Nov",
        '12' : "Dec"
    }
    now = datetime.now()
    today = now.strftime("%d-%m-%Y")
    today = today.split('-')
    number_of_month = today[1]
    month_name = str(month[number_of_month])
    num_day = str(today[0])
    num_year = str(today[2])
    date_to_save = f'{num_day} {month_name} {num_year}'
    return str(date_to_save)


#сохранять историю в json строку в БД дефект "номер" включен/отключен "дата"
def store_defect_history(status):
    date = take_date()
    defect_history = {
        status: date
        }    
    return defect_history

#print(store_defect_history('off'))