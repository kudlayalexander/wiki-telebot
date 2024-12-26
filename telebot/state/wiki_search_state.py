from aiogram.fsm.state import StatesGroup, State


class WikiSearchState(StatesGroup):
    key_phrase = State()
    article = State()