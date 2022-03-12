from aiogram.types import CallbackQuery
from keyboards import menu_callback
from loader import dp


# узнаём баланс
@dp.callback_query_handler(menu_callback.filter(btn='about_us'))
async def about_us(call: CallbackQuery):
    text = 'О НАС:\n' \
           'Автор: Ляушкин Ярослав Игоревич\n' \
           'ИНН: 781434668402\n' \
           '\n' \
           'КОНТАКТЫ:\n' \
           'Email: y.layshkin@gmail.com\n' \
           'Телефон: +7-905-220-31-50\n' \
           '\n' \

    await call.answer(text, show_alert=True)
   