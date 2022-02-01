from aiogram.dispatcher.filters.state import State, StatesGroup


class Task(StatesGroup):
    need_image_question = "Добавить изображение к сообщению?"
    set_text_question = "Напиши текст своего сообщения"
    set_image_question = "Выбери нужное изобрадение и отправь его мне"
    check_before_send = 'Вот твоё сообщение, проверь перед отправкой'
    need_image = State()
    set_text = State()
    set_image = State()
    choise = State()
    task_type = State()
