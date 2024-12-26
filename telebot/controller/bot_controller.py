import asyncio
from http.client import responses

from wiki.wiki_service import WikiService
from llm.cohere_service import CohereService
from aiogram.types import Message, CallbackQuery
from aiogram.utils.chat_action import ChatActionSender
from aiogram.fsm.context import FSMContext
from aiogram import Bot
from telebot.state.wiki_search_state import WikiSearchState
from wiki.dto.wiki_responses_dto import SearchResultElement
from typing import List
from telebot.service.inline_button_service import ButtonService

class BotController:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.wiki_service = WikiService()
        self.cohere_service = CohereService()
        self.inline_button_service = ButtonService()

    async def handle_search_start_message(self, message: Message, state: FSMContext) -> None:
        async with ChatActionSender.typing(bot=self.bot, chat_id=message.chat.id):
            await asyncio.sleep(1)
            await message.answer("Введите запрос по которому хотите найти статьи:")
        await state.set_state(WikiSearchState.key_phrase)

    async def handle_search_enter_key_phrase_message(self, message: Message, state: FSMContext) -> None:
        key_phrase: str = message.text
        await state.update_data(key_phrase=message.text)

        async with ChatActionSender.typing(bot=self.bot, chat_id=message.chat.id):
            search_results: List[SearchResultElement] = await self.wiki_service.get_pages_by_user_search(search_string=key_phrase)
            # search_results: List[SearchResultElement] = [SearchResultElement(title='123', url='asdas', ident='first', annotation='asdas'),
            #                                              SearchResultElement(title='456', url='dflskjgldfk', ident='second', annotation='dfklgbndlbdlfnkb'),]

            if len(search_results) == 0:
                await message.answer("По вашему запросу ничего не найдено")
                await state.clear()
                return

            response, inline_markup = self.inline_button_service.build_inline_buttons_and_response_by_search_results(search_results=search_results)

            await message.answer(text=f"По вашему запросу найдено:\n{response}", reply_markup=inline_markup)
            await state.clear()

    async def handle_search_find_page_message(self, callback: CallbackQuery, state: FSMContext) -> None:
        await state.clear()
        await callback.answer()

        page_ident: str = callback.data.replace(ButtonService.get_search_result_button_ident(), '')

        async with ChatActionSender.typing(bot=self.bot, chat_id=callback.message.chat.id):
            response: str = await self.wiki_service.get_text_from_page(page_ident=page_ident)

            await callback.message.answer(response)
            await callback.message.delete()

    async def handle_home(self, callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await callback.message.delete()
        await state.clear()

