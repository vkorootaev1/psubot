from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from language_ru_en import *


def get_menu(user_language):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    if user_language == "language_ru":
        b1 = KeyboardButton(text=text_change_language_ru)
        b2 = KeyboardButton(text=text_restart_bot_ru)
        b3 = KeyboardButton(text=text_help_ru)
        b4 = KeyboardButton(text=text_support_ru)

    else:
        b1 = KeyboardButton(text=text_change_language_en)
        b2 = KeyboardButton(text=text_restart_bot_en)
        b3 = KeyboardButton(text=text_help_en)
        b4 = KeyboardButton(text=text_support_en)

    kb.add(b1, b2).add(b3, b4)

    return kb



