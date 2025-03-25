from datetime import datetime

def take_date():
    month = {
        '01' : 'января',
        '02' : 'февраля',
        '03' : 'марта',
        '04' : 'апреля',
        '05' : 'мая',
        '06' : 'июня',
        '07' : 'июля',
        '08' : 'августа',
        '09' : 'сентября',
        '10' : 'октября',
        '11' : 'ноября',
        '12' : 'декабря'
    }
    now = datetime.now()
    today = now.strftime("%d-%m-%Y")
    today = today.split('-')
    number_of_month = today[1]
    month_name = month[number_of_month]
    date_to_save = f'{today[0] } {month_name} {today[2]}'
    return date_to_save


#сохранять историю в json строку в БД дефект "номер" включен/отключен "дата"
def store_defect_history(status):
    date = take_date()
    defect_history = {
        status: date
        }    
    return defect_history

#print(store_defect_history('off'))