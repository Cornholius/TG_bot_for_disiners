from aiogram.dispatcher.filters.state import State, StatesGroup


class Task(StatesGroup):
    set_text_question = "текст рассылки"
    set_image_question = "прикрепить изображение"
    # question3 = "Сумма вознаграждения?"
    task_complete = '''Я размещу Ваше объявление в нашей группе t.me/CornTest В комментариях под Вашим объявлением исполнители желающие взяться за заказ оставят свои комментарии'''
    set_text = State()
    set_image = State()
    all_images = []
    # answer3 = State()


class Payment(StatesGroup):
    answer1 = State()
    question1 = "Укажите сумму к оплате"