import asyncio

from aiogram import Dispatcher, types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import Throttled


class ThrottlingMiddleware(BaseMiddleware):

    def __init__(self, limit: int = 1):
        BaseMiddleware.__init__(self)
        self.rate_limit = limit

    async def on_process_message(self, message: types.Message, data: dict):
        dp = Dispatcher.get_current()

        try:
            await dp.throttle(key='antiflood_message', rate=self.rate_limit)
        except Throttled as t:
            await self.message_throttled(message=message, throttled=t)
            raise CancelHandler()

    async def message_throttled(self, message: types.Message, throttled: Throttled):
        delta = throttled.rate - throttled.delta
        if throttled.exceeded_count <= 2:
            await message.answer('<b>Вы пишите очень часто!\nПожалуйста, подождите несколько секунд!</b>', parse_mode='HTML')
        await asyncio.sleep(delta)
