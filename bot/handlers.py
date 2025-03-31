from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
#from work_with_csv import *
from db import *
from config import ALLOWED_USERS

router = Router()
class UserInput(StatesGroup):
    on = State()
    off = State()
    status = State()
    history = State()
    info = State()

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

@router.message(Command("defect_info"))
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