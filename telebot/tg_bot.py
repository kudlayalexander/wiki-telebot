from telebot.router.bot_router import BotRouter
from aiogram import Bot, Dispatcher


class TgBot:
    def __init__(self, token: str):
        self.bot = Bot(token=token)
        self.dispatcher = Dispatcher()
        self.bot_router = BotRouter(dispatcher=self.dispatcher, bot=self.bot)

    async def run(self):
        self.register_endpoints()
        await self.dispatcher.start_polling(self.bot)

    def register_endpoints(self):
        self.bot_router.register_basic_endpoints()
        self.bot_router.register_search_endpoints()