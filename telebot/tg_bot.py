from aiogram import Bot, Dispatcher

from telebot.router.bot_router import BotRouter


class TgBot:
    def __init__(self, bot_router: BotRouter, bot: Bot, dispatcher: Dispatcher):
        self.bot = bot
        self.dispatcher = dispatcher
        self.bot_router = bot_router

    async def run(self):
        self.register_endpoints()
        await self.dispatcher.start_polling(self.bot)

    def register_endpoints(self):
        self.bot_router.register_basic_endpoints()
        self.bot_router.register_search_endpoints()
