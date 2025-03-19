""" from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder

menu = [
    [InlineKeyboardButton(text="Включить дефект", callback_data="on"),
    InlineKeyboardButton(text="Отключить дефект", callback_data="off")],
    [InlineKeyboardButton(text="Статус", callback_data="status"),
    InlineKeyboardButton(text="История", callback_data="history")]
]
menu = InlineKeyboardMarkup(inline_keyboard=menu)
exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Выйти в меню")]], resize_keyboard=True)
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]])
builder = InlineKeyboardBuilder()
builder.button(text = f”Кнопка {i}”, callback_data=f”button_{i}”)
builder.adjust(2)
await msg.answer(“Текст сообщения”, reply_markup=builder.as_markup()) """