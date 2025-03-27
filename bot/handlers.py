from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from .work_with_csv import *

#import menu
#хорошо было бы прикрутить менюшку, дабы не прописывать возможные варианты работы с дефектами ручками
router = Router()
class UserInput(StatesGroup):
    on = State()
    off = State()
    status = State()
    history = State()

@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer("Привет! Я помогу с включением и отключением дефектов, а также получению информации по их состоянию")#, reply_markup=menu.menu

@router.message(Command("on"))
async def which_defect_on(msg: Message, state: FSMContext):
    await msg.answer("Какой дефект включить?")
    await state.set_state(UserInput.on)

@router.message(UserInput.on)
async def defect_on(message: Message, state: FSMContext):
    if message.text:
        await message.answer(f"Дефект: {message.text}\n{update_status(message.text, "on")}")
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
        await message.answer(f"Дефект: {message.text}\n{update_status(message.text, "off")}")
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