from aiogram import Dispatcher
from aiogram.filters import Command

from telebot.controller.bot_controller import BotController
from telebot.service.button_service import ButtonService
from telebot.state.wiki_search_state import WikiSearchState


class BotRouter:
    def __init__(self, dispatcher: Dispatcher, bot_controller: BotController):
        self.dispatcher: Dispatcher = dispatcher
        self.bot_controller: BotController = bot_controller

    def register_basic_endpoints(self):
        self.dispatcher.callback_query.register(self.bot_controller.handle_home,
                                                lambda callback: callback and str(callback.data).startswith(ButtonService.get_home_button_ident()))

    def register_search_endpoints(self) -> None:
        self.dispatcher.message.register(
            self.bot_controller.handle_search_start_message, Command("search"))
        self.dispatcher.message.register(
            self.bot_controller.handle_search_enter_key_phrase_message, WikiSearchState.key_phrase)
        self.dispatcher.callback_query.register(self.bot_controller.handle_search_find_page_message,
                                                lambda callback: callback and str(callback.data).startswith(ButtonService.get_search_result_button_ident()))
