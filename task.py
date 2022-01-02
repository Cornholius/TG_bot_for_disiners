from aiogram.dispatcher.filters.state import State, StatesGroup


class Task(StatesGroup):
    question1 = "Как мне Вас представить?"
    question2 = "Изложите суть задачи (напишите ТЗ)"
    question3 = "Сумма вознаграждения?"
    task_complete = '''Я размещу Ваше объявление в нашей группе t.me/CornTest В комментариях под Вашим объявлением исполнители желающие взяться за заказ оставят свои комментарии'''
    answer1 = State()
    answer2 = State()
    answer3 = State()
