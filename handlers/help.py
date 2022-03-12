from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ContentType
from keyboards import back_to_main_menu, cancel_menu, menu_callback
from loader import dp, bot, db, test_payload_token
from logic.clear_mesages import cleaner
from states import Payment


# узнаём баланс
@dp.callback_query_handler(menu_callback.filter(btn='rtfm'))
async def rtfm(call: CallbackQuery):
    text = 'Для возврата средств необходимо связаться с нами написав на почту: y.layshkin@gmail.com\n' \
           '\n' \
           'Возврат средств осуществляется в течение 10 дней в соответствии с действующим законодательством'

    await call.answer(text, show_alert=True)
