from wiki.dto.wiki_responses_dto import SearchResultElement
from typing import List
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

class ButtonService:
    def __init__(self):
        self.digit_emojis = {
            '0': '0️⃣',
            '1': '1️⃣',
            '2': '2️⃣',
            '3': '3️⃣',
            '4': '4️⃣',
            '5': '5️⃣',
            '6': '6️⃣',
            '7': '7️⃣',
            '8': '8️⃣',
            '9': '9️⃣'
        }

    def build_inline_buttons_and_response_by_search_results(self, search_results: List[SearchResultElement]) -> (str, InlineKeyboardMarkup):
        keyboard_markup: InlineKeyboardMarkup = self.__build_inline_buttons_by_search_results(search_results)
        response: str = self.__build_response_by_search_results(search_results)

        return response, keyboard_markup


    def __build_inline_buttons_by_search_results(self, search_results: List[SearchResultElement]) -> InlineKeyboardMarkup:
        inline_keyboard: List[List[InlineKeyboardButton]] = []
        counter = 1

        for search_result in search_results:
            button: List[InlineKeyboardButton] = []

            text: str = self.__convert_to_emoji_number(counter)
            callback_data = ButtonService.get_search_result_button_ident() + search_result.ident

            inline_button = InlineKeyboardButton(
                text=text,
                callback_data=callback_data
            )

            button.append(inline_button)
            inline_keyboard.append(button)

            counter += 1

        inline_keyboard.append([self.__create_home_button()])

        return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    def __build_response_by_search_results(self, search_results: List[SearchResultElement]) -> str:
        counter: int = 1
        responses: List[str] = []

        for search_result in search_results:
            emoji = self.__convert_to_emoji_number(counter)

            response = f"{emoji} {search_result.title}\n{search_result.annotation}\nСсылка: {search_result.url}"

            counter += 1
            responses.append(response)

        return '\n'.join(responses)

    def __convert_to_emoji_number(self, num: int) -> str:
        return ''.join(self.digit_emojis[digit] for digit in str(num))

    def __create_home_button(self) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            text="Домой",
            callback_data=ButtonService.get_search_result_button_ident()
        )

    @staticmethod
    def get_home_button_ident() -> str:
        return "HOME_"

    @staticmethod
    def get_search_result_button_ident() -> str:
        return "SR_"