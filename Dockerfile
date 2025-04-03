FROM python:3.12

WORKDIR /app

COPY bot/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Копируем код бота внутрь контейнера
COPY bot/ .

# Делаем скрипт запуска исполняемым
RUN chmod +x entrypoint.sh

# Запускаем скрипт при старте контейнера
CMD ["./entrypoint.sh"]