from aiogram import types, F, Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from db import *
from config import ALLOWED_USERS
from dict_of_defects.compare_dict import get_message_about_updates, update_dict

router = Router()
class UserInput(StatesGroup):
    on = State()
    off = State()
    status = State()
    history = State()
    info = State()
    confirm_update_dict = State()

# Фильтр доступа
@router.message(lambda message: message.from_user.id not in ALLOWED_USERS)
async def access_denied(message: Message):
    await message.answer("⛔ Доступ запрещён. Вы не в списке разрешённых пользователей.")

@router.message(CommandStart("start"))
async def start_handler(msg: Message):
    #active_users.add(msg.from_user.id)
    await msg.answer("Привет! Я помогу с включением и отключением дефектов, а также получению информации по их состоянию")
    
@router.message(Command("on"))
async def which_defect_on(msg: Message, state: FSMContext):
    await msg.answer("Какой дефект включить?")
    await state.set_state(UserInput.on)

@router.message(UserInput.on)
async def defect_on(message: Message, state: FSMContext):
    if message.text:
        await message.answer(f"Дефект: {message.text}\n{update_status(message.text, 'on')}")
        await state.clear()
    else:
        await message.answer("Пожалуйста, введите дефект")
    
@router.message(Command("off"))
async def  which_defect_off(msg: Message, state: FSMContext):
    await msg.answer("Какой дефект отключить?")
    await state.set_state(UserInput.off)

@router.message(UserInput.off)
async def defect_off(message: Message, state: FSMContext):
    if message.text:
        await message.answer(f"Дефект: {message.text}\n{update_status(message.text, 'off')}")
        await state.clear()
    else:
        await message.answer("Пожалуйста, введите дефект")

@router.message(Command("status"))
async def status_handler(msg: Message, state: FSMContext):
    await msg.answer("По какому дефекту нужен статус работы?")
    await state.set_state(UserInput.status)

@router.message(UserInput.status)
async def status(message: Message, state: FSMContext):
    if message.text:
        await message.answer(f"Дефект: {message.text}\n{get_status(message.text)}")
        await state.clear()
    else:
        await message.answer("Пожалуйста, введите дефект")

@router.message(Command("history"))
async def history_handler(msg: Message, state: FSMContext):
    await msg.answer("По какому дефекту нужна история статусов?")
    await state.set_state(UserInput.history)

@router.message(UserInput.history)
async def history(message: Message, state: FSMContext):
    if message.text:
        await message.answer(f"Дефект: {message.text}\n{show_history(message.text)}")
        await state.clear()
    else:
        await message.answer("Пожалуйста, введите дефект")

@router.message(Command("defect_info"))# обращается к питоновскому словарю, не к БД
async def defect_info_handler(msg: Message, state: FSMContext):
    await msg.answer("для какого дефекта нужен код или название по коду?")
    await state.set_state(UserInput.info)

@router.message(UserInput.info)
async def defect_info(message: Message, state: FSMContext):
    if message.text:
        await message.answer(f"По запросу: {message.text}\n{get_defect_info(message.text)}")
        await state.clear()
    else:
        await message.answer("Пожалуйста, введите дефект")

@router.message(Command("check_updates"))# получает данные из таблицы в гугле и сравнивает с имеющимися
async def defect_info_handler(msg: Message):
    await msg.answer(f"{get_message_about_updates()}")

@router.message(Command("update_dict"))# запрашивает подтверждение на обновление словаря и обновляет при подтверждении
async def defect_info_handler(msg: Message, state: FSMContext):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="ДА"), KeyboardButton(text="НЕТ")]
        ],
        resize_keyboard=True,  # Подгоняем размер кнопок
        one_time_keyboard=True  # Скрываем после нажатия
    )
    await msg.answer('Вы уверены, что хотите обновить словарь кодов и названий дефектов?', reply_markup=keyboard)
    await state.set_state(UserInput.confirm_update_dict)

@router.message(UserInput.confirm_update_dict)
async def defect_info(message: Message, state: FSMContext):
    if message.text.lower() == 'да':
        await message.answer(f"{update_dict()}", reply_markup=ReplyKeyboardRemove())
        await state.clear()
    else:
        await message.answer("Вы отказались обновлять словарь дефектов", reply_markup=ReplyKeyboardRemove())
        await state.clear()
    
