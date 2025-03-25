from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from .utils.save_defect_history import *

#import menu
#хорошо было бы прикрутить менюшку, дабы не прописывать возможные варианты работы с дефектами ручками
router = Router()
class UserInput(StatesGroup):
    number = State()
    text = State()
    string = State()

@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer("Привет! Я помогу с включением и отключением дефектов, а также получению информации по их состоянию")#, reply_markup=menu.menu

@router.message(Command("put_number"))
async def ask_number(message: Message, state: FSMContext):
    await message.answer("Введите число:")
    await state.set_state(UserInput.number)

@router.message(Command("on"))
async def which_defect_on(msg: Message, state: FSMContext):
    await msg.answer("Какой дефект включить?")
    await state.set_state(UserInput.string)

@router.message(UserInput.string)
async def defect_on(message: Message, state: FSMContext):
    if message.text:
        await message.answer(f"Вы ввели число: {message.text}\n{store_defect_history("on")}")
        await state.clear()
    else:
        await message.answer("Пожалуйста, введите дефект")
    
""" 
ДОБАВИТЬ ОБРАБОТЧИКИ ВСЕХ КОМАНД С ДОСТАВАНИЕМ ИЗ CSV

@router.message(Command("off"))
async def  which_defect_off(msg: Message, state: FSMContext):
    await msg.answer("Какой дефект отключить?")
    await state.set_state(UserInput.string)

@router.message(UserInput.string)
async def defect_on(message: Message, state: FSMContext):
    if message.text:
        await message.answer(f"Вы ввели число: {message.text}\n{store_defect_history("on")}")
        await state.clear()
    else:
        await message.answer("Пожалуйста, введите дефект")

@router.message(Command("status"))
async def start_handler(msg: Message):
    await msg.answer("По какому дефекту нужен статус работы?")

@router.message(Command("history"))
async def start_handler(msg: Message):
    await msg.answer("По какому дефекту нужна история статусов?") """