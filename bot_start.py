import asyncio
import logging
import os

import dotenv
from aiogram import Bot, Dispatcher

from llm.cohere_requests import CohereRequests
from llm.cohere_service import CohereService
from telebot.controller.bot_controller import BotController
from telebot.router.bot_router import BotRouter
from telebot.service.inline_button_service import ButtonService
from telebot.tg_bot import TgBot
from wiki.wiki_requests import WikiRequests
from wiki.wiki_service import WikiService


def main():
    dotenv.load_dotenv(dotenv_path=".env")

    logging.basicConfig(level=logging.DEBUG)

    cohere_api_key: str = os.getenv("COHERE_API_KEY")
    wiki_api_url: str = os.getenv("WIKI_API_URL")
    tg_api_token: str = os.getenv("TG_BOT_API_KEY")

    wiki_requests: WikiRequests = WikiRequests(wiki_api_url)
    wiki_service: WikiService = WikiService(wiki_requests)

    cohere_requests: CohereRequests = CohereRequests(cohere_api_key)
    cohere_service: CohereService = CohereService(cohere_requests)

    bot: Bot = Bot(token=tg_api_token)
    dispatcher: Dispatcher = Dispatcher()
    inline_button_service: ButtonService = ButtonService()

    bot_controller: BotController = BotController(
        bot, wiki_service, cohere_service, inline_button_service)

    bot_router: BotRouter = BotRouter(dispatcher, bot_controller)

    tg_bot: TgBot = TgBot(bot_router, bot, dispatcher)

    asyncio.run(tg_bot.run())


if __name__ == '__main__':
    main()
