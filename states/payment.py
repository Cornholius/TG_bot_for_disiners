from aiogram.dispatcher.filters.state import StatesGroup, State


class Payment(StatesGroup):
    answer1 = State()
    question1 = "Укажите сумму к оплате. Минимальная сумма 100р."
