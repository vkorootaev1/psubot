import os
import django
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from fuzzywuzzy import process
from channels.db import database_sync_to_async
from keyboards_menu import get_menu
from aiogram.dispatcher.filters import Text
from antiflood import ThrottlingMiddleware
from bot_settings import TOKEN_API
from language_ru_en import *

os.environ['DJANGO_SETTINGS_MODULE'] = 'psubot.settings'
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "True"
django.setup()

from psutelegrambot.models import Question, TelegramUser, UserNotFoundQuestion

storage = MemoryStorage()

bot = Bot(TOKEN_API)

dp = Dispatcher(bot, storage=storage)


# Сообщение, которое выводится при запуске бота
async def on_startup(_):
    print('Бот запущен!')


# Нахождение всех наследников заданной вершины
@database_sync_to_async
def get_all_children(parent_id):
    return Question.objects.filter(parent_id=parent_id)


# Нахождение id вопроса среди всех корней деревьев
# с использованием библиотеки нечеткого поиска
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


# Является ли вершина листом
@database_sync_to_async
def isLeaf(question_id):
    return 0 if Question.objects.filter(parent_id=question_id).exists() else 1


# Нахождение всех предыдущих вопросов и ответа, на который нажал пользователь
# Нужно для отрисовки пользователю
# (Избыточно, нужно переделать)
def get_previous_questions_with_answer(question_id):
    previous_answer = Question.objects.get(id=question_id)
    previous_questions = Question.objects.filter(parent_id=previous_answer.parent_id)
    return previous_answer, previous_questions


# Создание или обновление пользовательской информации в БД (языка)
@database_sync_to_async
def create_or_update_user_information(user_id, language_code, first_name, last_name, username):
    obj, created = TelegramUser.objects.update_or_create(
        user_id=user_id, defaults={"language_code": language_code, "first_name": first_name, "last_name": last_name, "username": username}
    )


# Получение языка пользователя
# 0 - русский, 1 - английский
@database_sync_to_async
def get_user_language(user_id):
    current_user = TelegramUser.objects.get(user_id=user_id)
    return current_user.language_code


# Обработчик события на команду 'start'
@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message):
    await change_language_button_menu(message)


# Обработчик события на команду 'помощь'
@dp.message_handler(Text(equals=["Помощь", 'Help']))
async def help_button_menu(message: types.Message):
    user_language_code = await get_user_language(message.from_user.id)
    await message.answer(text=help_text_ru_description if user_language_code == 0 else help_text_en_description,
                         parse_mode='HTML')


# Обработчик события на команду 'сменить язык'
@dp.message_handler(Text(equals=["Сменить язык", "Change language"]))
async def change_language_button_menu(message: types.Message):
    ikb = InlineKeyboardMarkup()
    ikb.add(InlineKeyboardButton(text='Русский язык', callback_data='language_ru'))
    ikb.add(InlineKeyboardButton(text='English language', callback_data='language_en'))
    await message.answer(text='<b>Выберите ваш язык:\nChoose your language:</b>', reply_markup=ikb, parse_mode='HTML')


# Обработчик события на команду 'перезапуск бота'
@dp.message_handler(Text(equals=["Перезапустить бота", "Restart bot"]))
async def restart_bot_menu(message: types.Message):
    await start_bot(message)


# Обработчик события на команду 'техподдержка'
@dp.message_handler(Text(equals=["Техподдержка", "Support"]))
async def support_menu(message: types.Message):
    user_language_code = await get_user_language(message.from_user.id)
    ikb = InlineKeyboardMarkup()
    ikb.add(InlineKeyboardButton(text=text_support_write_ru if user_language_code == 0 else text_support_write_en,
                                 url='https://t.me/johnkorotaev'))
    await message.answer(text=text_support_button_ru if user_language_code == 0 else text_support_button_en,
                         reply_markup=ikb, parse_mode='HTML')


# Смена пользовательского интерфейса на выбранный язык пользователя
@dp.callback_query_handler(lambda c: c.data in ['language_ru', 'language_en'])
async def change_language(callback: types.CallbackQuery):
    first_name = callback.from_user.first_name if callback.from_user.first_name is not None else ""
    last_name = callback.from_user.last_name if callback.from_user.last_name is not None else ""
    username = callback.from_user.username if callback.from_user.username is not None else ""
    if callback.data == 'language_ru':
        await create_or_update_user_information(callback.from_user.id, 0, first_name, last_name, username)
    else:
        await create_or_update_user_information(callback.from_user.id,1, first_name, last_name, username)
    await bot.edit_message_text(chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                text=text_changed_language_ru if callback.data == 'language_ru' else text_changed_language_en,
                                parse_mode='HTML',
                                )
    await bot.send_message(text=text_start_bot_ru if callback.data == 'language_ru' else text_start_bot_en,
                           reply_markup=get_menu(callback.data), chat_id=callback.from_user.id, parse_mode='HTML')


# Обработчик на 1 вопрос пользователя, который задается пользователем с клавиатуры
# и обрабатывается с алгоритмами нечеткого поиска
@dp.message_handler(content_types="text")
async def first_question(message: types.Message):
    try:
        user_language_code = await get_user_language(message.from_user.id)

        question_id_by_fuzzy_search = await get_question_id(message.text, user_language_code)

        if question_id_by_fuzzy_search:

            answers = await get_all_children(question_id_by_fuzzy_search)

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

            UserNotFoundQuestion(
                user_id=message.from_user.id,
                message_id=message.message_id,
                text=message.text
            ).save()
    except:
        await change_language_button_menu(message)


# Функция, которая редактирует сообщение
# Для того, чтобы пользователь мог увидеть,
# на какую кнопку с ответом он нажал
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


# Обработчик, который генерирует кнопки с выбором ответов,
# чтобы дальше продвигаться по дереву решений
@dp.callback_query_handler()
async def questions_buttons(callback: types.CallbackQuery):
    user_language_code = await get_user_language(callback.from_user.id)

    inline_answers = await get_all_children(callback.data)

    if await isLeaf(inline_answers[0]):

        if user_language_code == 0:
            the_end_answer = inline_answers[0].text_ru
            text = text_answer_ru + '</u>' + the_end_answer + '</b>'
        else:
            the_end_answer = inline_answers[0].text_en
            text = text_answer_en + '</u>' + the_end_answer + '</b>'

        await callback.message.answer(
            text=text,
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

    text = edit_text(callback.data, user_language_code)

    await bot.edit_message_text(chat_id=callback.from_user.id, message_id=callback.message.message_id, text=text,
                                parse_mode='HTML')


async def replyUserMessage(user_id, reply_to_message_id):
    await bot.send_message(user_id, 'Ваш вопрос был успешно добавлен!', reply_to_message_id=reply_to_message_id)


# Запуск бота
if __name__ == '__main__':
    dp.middleware.setup(ThrottlingMiddleware())
    executor.start_polling(dp, on_startup=on_startup)
