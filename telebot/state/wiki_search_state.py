from aiogram.fsm.state import State, StatesGroup


class WikiSearchState(StatesGroup):
    key_phrase = State()
    article = State()
