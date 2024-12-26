import asyncio
import logging
from telebot.tg_bot import TgBot
import dotenv
import os


def main():
    dotenv.load_dotenv(dotenv_path=".env")
    tg_api_token: str = os.getenv("TG_BOT_API_KEY")
    bot = TgBot(token=tg_api_token)

    asyncio.run(bot.run())

if __name__ == '__main__':
    main()