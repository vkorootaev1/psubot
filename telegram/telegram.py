import datetime
import os
import django
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from fuzzywuzzy import process
from language_ru_en import *
from channels.db import database_sync_to_async
from keyboards_menu import get_menu
from aiogram.dispatcher.filters import Text
from antiflood import ThrottlingMiddleware
from bot_settings import TOKEN_API

os.environ['DJANGO_SETTINGS_MODULE'] = 'psubot.settings'
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "True"
django.setup()

from psutelegrambot.models import Question, TelegramUser

storage = MemoryStorage()

bot = Bot(TOKEN_API)

dp = Dispatcher(bot, storage=storage)


async def on_startup(_):
    print('Бот запущен!')


@database_sync_to_async
def get_all_questions(parent_id):
    return Question.objects.filter(parent_id=parent_id)


@database_sync_to_async
def get_question_id(text, user_language):
    possible_questions = Question.objects.filter(parent_id=None)
    if user_language == 0:
        greatest_match = process.extractOne(text, [i.text_ru for i in possible_questions], score_cutoff=70)
        if greatest_match:
            return [i.id for i in possible_questions if i.text_ru == greatest_match[0]][0]
    elif user_language == 1:
        greatest_match = process.extractOne(text, [i.text_en for i in possible_questions], score_cutoff=70)
        if greatest_match:
            return [i.id for i in possible_questions if i.text_en == greatest_match[0]][0]

    return 0


@database_sync_to_async
def isLeaf(question_id):
    return 0 if Question.objects.filter(parent_id=question_id).exists() else 1


@database_sync_to_async
def get_question_by_id(question_id):
    return Question.objects.get(id=question_id)


def get_previous_questions_with_answer(question_id):
    previous_answer = Question.objects.get(id=question_id)
    previous_questions = Question.objects.filter(parent_id=previous_answer.parent_id)
    return previous_answer, previous_questions


@database_sync_to_async
def create_or_update_user_information(user_id, language_code):
    obj, created = TelegramUser.objects.update_or_create(
        user_id=user_id, defaults={"language_code": language_code}
    )


@database_sync_to_async
def get_user_language(user_id):
    current_user = TelegramUser.objects.get(user_id=user_id)
    return current_user.language_code


@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message):
    await change_language_button_menu(message)


@dp.message_handler(Text(equals=["Помощь", 'Help']))
async def help_button_menu(message: types.Message):
    user_language_code = await get_user_language(message.from_user.id)
    await message.answer(text=help_text_ru_description if user_language_code == 0 else help_text_en_description,
                         parse_mode='HTML')


@dp.message_handler(Text(equals=["Сменить язык", "Change language"]))
async def change_language_button_menu(message: types.Message):
    ikb = InlineKeyboardMarkup()
    ikb.add(InlineKeyboardButton(text='Русский язык', callback_data='language_ru'))
    ikb.add(InlineKeyboardButton(text='English language', callback_data='language_en'))
    await message.answer(text='<b>Выберите ваш язык:\nChoose your language:</b>', reply_markup=ikb, parse_mode='HTML')


@dp.message_handler(Text(equals=["Перезапустить бота", "Restart bot"]))
async def restart_bot_menu(message: types.Message):
    await start_bot(message)


@dp.message_handler(Text(equals=["Техподдержка", "Support"]))
async def support_menu(message: types.Message):
    user_language_code = await get_user_language(message.from_user.id)
    ikb = InlineKeyboardMarkup()
    ikb.add(InlineKeyboardButton(text=text_support_write_ru if user_language_code == 0 else text_support_write_en,
                                 url='https://t.me/johnkorotaev'))
    await message.answer(text=text_support_button_ru if user_language_code == 0 else text_support_button_en,
                         reply_markup=ikb, parse_mode='HTML')


@dp.callback_query_handler(lambda c: c.data in ['language_ru', 'language_en'])
async def change_language(callback: types.CallbackQuery):
    if callback.data == 'language_ru':
        await create_or_update_user_information(callback.from_user.id, 0)
    else:
        await create_or_update_user_information(callback.from_user.id, 1)
    await bot.edit_message_text(chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                text=text_changed_language_ru if callback.data == 'language_ru' else text_changed_language_en,
                                parse_mode='HTML',
                                )
    await bot.send_message(text=text_start_bot_ru if callback.data == 'language_ru' else text_start_bot_en,
                           reply_markup=get_menu(callback.data), chat_id=callback.from_user.id, parse_mode='HTML')


@dp.message_handler(content_types="text")
async def questions(message: types.Message):
    user_language_code = await get_user_language(message.from_user.id)

    question_id_by_fuzzy_search = await get_question_id(message.text, user_language_code)

    if question_id_by_fuzzy_search:

        answers = await get_all_questions(question_id_by_fuzzy_search)

        ikb = InlineKeyboardMarkup()

        for answer in answers:

            if user_language_code == 0:
                inline_button_text = answer.text_ru
            else:
                inline_button_text = answer.text_en

            ikb.add(InlineKeyboardButton(text=inline_button_text, callback_data=answer.id))

        await message.answer(text=text_choose_ru if user_language_code == 0 else text_choose_en, reply_markup=ikb,
                             parse_mode='HTML')

    else:
        await message.answer(text=text_not_answer_found_ru if user_language_code == 0 else text_not_answer_found_en,
                             parse_mode='HTML')
        reply_to_support = f"От пользователя: {message.from_user.id}\nТекст сообщения: {message.text}\nВремя: {datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}"
        await bot.send_message(chat_id='-1001712899180', text=reply_to_support)


def edit_text(previous_question_id, user_language_code):
    edit_text = text_choose_ru if user_language_code == 0 else text_choose_en

    previous_answer, previous_questions = get_previous_questions_with_answer(previous_question_id)

    for pr_question in previous_questions:

        if user_language_code == 0:
            pr_question_text = pr_question.text_ru
        else:
            pr_question_text = pr_question.text_en

        edit_text += '\n● ' + str(pr_question_text)

    edit_text += text_choosed_answer_ru + previous_answer.text_ru + '</u></b>' if user_language_code == 0 else text_choosed_answer_en + previous_answer.text_en + '</u></b>'

    return edit_text


@dp.callback_query_handler()
async def questions_buttons(callback: types.CallbackQuery):
    user_language_code = await get_user_language(callback.from_user.id)

    inline_answers = await get_all_questions(callback.data)

    if await isLeaf(inline_answers[0]):

        if user_language_code == 0:
            the_end_answer = inline_answers[0].text_ru
        else:
            the_end_answer = inline_answers[0].text_en

        await callback.message.answer(
            text=text_answer_ru + '</u>' + the_end_answer + '</b>' if user_language_code == 0 else text_answer_en + '</u>' + the_end_answer + '</b>',
            parse_mode='HTML')

    else:

        ikb = InlineKeyboardMarkup()

        for inline_answer in inline_answers:

            if user_language_code == 0:
                inline_button_text = inline_answer.text_ru
            else:
                inline_button_text = inline_answer.text_en

            ikb.add(InlineKeyboardButton(text=inline_button_text, callback_data=inline_answer.id))

        await callback.message.answer(text=text_choose_ru if user_language_code == 0 else text_choose_en,
                                      reply_markup=ikb, parse_mode='HTML')

    # await bot.delete_message(
    #     chat_id=callback.from_user.id, message_id=callback.message.message_id)

    text = edit_text(callback.data, user_language_code)

    await bot.edit_message_text(chat_id=callback.from_user.id, message_id=callback.message.message_id, text=text,
                                parse_mode='HTML')


if __name__ == '__main__':
    dp.middleware.setup(ThrottlingMiddleware())
    executor.start_polling(dp, on_startup=on_startup)
