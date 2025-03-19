from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command

from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.types import Message

#import menu
#хорошо было бы прикрутить менюшку, дабы не прописывать возможные варианты работы с дефектами ручками
router = Router()

@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer("Привет! Я помогу с включением и отключением дефектов, а также получению информации по их состоянию")#, reply_markup=menu.menu

@router.message(Command("on"))
async def start_handler(msg: Message):
    await msg.answer("Какой дефект включить?")

@router.message(Command("off"))
async def start_handler(msg: Message):
    await msg.answer("Какой дефект отключить?")

@router.message(Command("status"))
async def start_handler(msg: Message):
    await msg.answer("По какому дефекту нужен статус работы?")

@router.message(Command("history"))
async def start_handler(msg: Message):
    await msg.answer("По какому дефекту нужна история статусов?")