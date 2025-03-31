#!/bin/bash
echo "Ожидание PostgreSQL..."
sleep 5  # Даём время базе данных запуститься

echo "Запуск бота..."
python bot.py