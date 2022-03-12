from aiogram.types import CallbackQuery
from keyboards import menu_callback
from loader import dp



# узнаём баланс
@dp.callback_query_handler(menu_callback.filter(btn='prices'))
async def prices(call: CallbackQuery):
    text = 'СТОИМОСТЬ УСЛУГ:\n' \
           '\n' \
           'Рассылка объявления подписчикам: 1,5р. за человека\n' \
           '\n' \
           'Размещение объявления в канале: бесплатно'

    await call.answer(text, show_alert=True)
