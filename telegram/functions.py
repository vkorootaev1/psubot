import asyncio

from aiogram import Bot

bot = Bot('6229683977:AAExh-HX6WKl_H_gV-byniMiIb62STdkuUg')


async def replyUserMessage(first_name: str, user_id: int, reply_to_message_id: int, language_code: int):
    new_session = await bot.get_session()
    if language_code == 0:
        reply_text = f'<b>Дорогой(ая), <u>{first_name}</u>. Вопрос, который вы задавали, был добавлен!</b>'
    elif language_code == 0:
        reply_text = f'<b>Dear, <u>{first_name}</u>. The question you asked has been added!</b>'
    await bot.send_message(user_id,
                           reply_text,
                           reply_to_message_id=reply_to_message_id, parse_mode='HTML')
    await new_session.close()


async def massMailingTelegramUsers(text_ru: str, text_en: str, users_id):
    new_session = await bot.get_session()
    for user_id in users_id:
        if user_id['language_code'] == 0 and len(text_ru):
            await bot.send_message(user_id['id'], text_ru)
        elif user_id['language_code'] == 1 and len(text_en):
            await bot.send_message(user_id['id'], text_en)
        await asyncio.sleep(0.1)
    await new_session.close()

