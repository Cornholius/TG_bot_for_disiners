from aiogram.dispatcher.filters.state import State, StatesGroup


class Task(StatesGroup):
    need_image_question = '''
                            В объявлении будут использоваться изображения? 
                            При нажатии кнопки 'Да' бот будет ожидать от Вас группу изображений от 2 до 10 
                            и не отстанет, пока вы ему их не скините
                            '''
    set_text_question = "текст рассылки"
    set_image_question = "прикрепить изображение"
    task_complete = '''
                        Я размещу Ваше объявление в нашей группе t.me/CornTest В комментариях под Вашим объявлением 
                        исполнители желающие взяться за заказ оставят свои комментарии
                        '''
    need_image = State()
    set_text = State()
    set_image = State()
    choise = State()
    bot_last_message = []


class Payment(StatesGroup):
    answer1 = State()
    question1 = "Укажите сумму к оплате. Минимальная сумма 100р. (100 - 250000)"
