import psycopg2

try:
    # пытаемся подключиться к базе данных
    conn = psycopg2.connect(dbname='defect_status', user='postgres', password='adventus', host='5432')
    print("connected")
except Exception as e:
    # в случае сбоя подключения будет выведено сообщение в STDOUT
    print(f'Can`t establish connection to database {e}')