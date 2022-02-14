from aiogram.dispatcher.filters.state import StatesGroup, State


class ImportContacts(StatesGroup):
    set_doc = State()
