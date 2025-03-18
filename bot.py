import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from processing_defect_for_request import process_defect

TOKEN = "ТВОЙ_ТОКЕН_ОТ_BOTFATHER"

# Создаем бота и диспатчер
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Обработчик входящих сообщений
@dp.message()
async def echo(message: types.Message):
    await message.answer(message.text)

# Запуск бота
async def main():
    logging.basicConfig(level=logging.INFO)
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
