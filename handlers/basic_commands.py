from aiogram import Router, F
from aiogram.filters.command import Command
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.keys_tasks import keys_menu

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    welcome_text ="""Привет! 👋 Я — твой верный помощник в организации дел!  

✨ Со мной ты сможешь:  
- Записывать задачи в пару кликов  
- Не забывать о важном  
- Чувствовать себя продуктивнее  

Давай наведем порядок в делах? Выбирай действие в меню!  """

    await message.answer(welcome_text, reply_markup=keys_menu())