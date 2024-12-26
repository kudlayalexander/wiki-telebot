from aiogram import Dispatcher, Bot, F
from aiogram.filters import Command
from telebot.controller.bot_controller import BotController
from telebot.state.wiki_search_state import WikiSearchState
from telebot.service.inline_button_service import ButtonService


class BotRouter:
    def __init__(self, dispatcher: Dispatcher, bot: Bot):
        self.dispatcher = dispatcher
        self.bot_controller = BotController(bot)

    def register_basic_endpoints(self):
        self.dispatcher.callback_query.register(self.bot_controller.handle_home,
                                                lambda callback: callback and str(callback.data).startswith(ButtonService.get_home_button_ident()))

    def register_search_endpoints(self) -> None:
        self.dispatcher.message.register(self.bot_controller.handle_search_start_message, Command("search"))
        self.dispatcher.message.register(self.bot_controller.handle_search_enter_key_phrase_message, WikiSearchState.key_phrase)
        self.dispatcher.callback_query.register(self.bot_controller.handle_search_find_page_message,
                                                lambda callback: callback and str(callback.data).startswith(ButtonService.get_search_result_button_ident()))