from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def keys_menu() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="✏️ Добавить задачу")
    kb.button(text="❌ Удалить задачу")
    kb.button(text="📃 Все задачи")

    kb.adjust(2, 1)
    return kb.as_markup(resize_keyboard=True)


def cancellations_task() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="❌ Отмена")

    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)