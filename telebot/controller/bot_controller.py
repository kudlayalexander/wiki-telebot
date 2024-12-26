import asyncio
import copy
from typing import List

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, ReplyKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.chat_action import ChatActionSender

from llm.cohere_service import CohereService
from telebot.service.button_service import ButtonService
from telebot.state.wiki_search_state import WikiSearchState
from wiki.dto.wiki_search_dtos import SearchResultElement
from wiki.wiki_service import WikiService

class BotController:
    def __init__(self, bot: Bot, wiki_service: WikiService, cohere_service: CohereService, inline_button_service: ButtonService):
        self.bot: Bot = bot
        self.wiki_service: WikiService = wiki_service
        self.cohere_service: CohereService = cohere_service
        self.inline_button_service: ButtonService = inline_button_service

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

            if len(search_results) == 0:
                await message.answer("По вашему запросу ничего не найдено")
                await state.clear()
                return

            response, inline_markup = self.inline_button_service.build_inline_buttons_and_response_by_search_results(
                search_results=search_results)

            await message.answer(text=f"По вашему запросу найдено:\n{response}", reply_markup=inline_markup)
            await state.clear()

    async def handle_search_find_page_message(self, callback: CallbackQuery, state: FSMContext) -> None:
        await callback.answer()
        await self.block_markup_buttons(callback)
        await state.clear()

        page_ident: str = callback.data.replace(
            ButtonService.get_search_result_button_ident(), '')

        async with ChatActionSender.typing(bot=self.bot, chat_id=callback.message.chat.id):
            wiki_page_text: str = await self.wiki_service.get_text_from_page(page_ident=page_ident)

            if await self.check_is_failed_and_unblock_markup(callback, wiki_page_text, "Не удалось получить текст страницы"):
                return

            summarized_text: str = await self.cohere_service.summarize_text(wiki_page_text)

            if await self.check_is_failed_and_unblock_markup(callback, summarized_text, "Не удалось суммировать текст"):
                return

            await callback.message.answer(summarized_text)
            await self.set_markup_buttons_callback_ident(callback.message.reply_markup.inline_keyboard,
                                                    ButtonService.get_search_result_button_ident())

    async def handle_home(self, callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await callback.message.delete()
        await state.clear()

    async def block_markup_buttons(self, callback: CallbackQuery) -> None:
        new_inline_keyboard: List[List[InlineKeyboardButton]] = callback.message.reply_markup.inline_keyboard
        await self.set_markup_buttons_callback_ident(new_inline_keyboard, "mock")

        await self.bot.edit_message_reply_markup(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            reply_markup=callback.message.reply_markup
        )

    async def set_markup_buttons_callback_ident(self, inline_keyboard: list[list[InlineKeyboardButton]], ident: str) -> None:
        for row in inline_keyboard:
            for button in row:
                if isinstance(button, InlineKeyboardButton):
                    await self.set_button_callback_ident(button, ident)

    async def set_button_callback_ident(self, button: InlineKeyboardButton, ident: str) -> None:
        button.callback_data = ident

    async def check_is_failed_and_unblock_markup(self, callback: CallbackQuery, text: str, msg: str) -> bool:
        if text != "FAILED":
            return False
        await self.set_markup_buttons_callback_ident(callback.message.reply_markup.inline_keyboard,
                                                     ButtonService.get_search_result_button_ident())
        await callback.message.answer(msg)
        return True

