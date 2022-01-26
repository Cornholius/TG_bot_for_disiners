from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards import main_menu
from keyboards.callback_datas import menu_callback
from loader import dp, bot
from logic.clear_mesages import clear_bot_messages


@dp.callback_query_handler(menu_callback.filter(btn='main_menu'))
async def to_main_menu(message: types.Message, state: FSMContext):
    await state.reset_state(with_data=True)
    await clear_bot_messages(message.from_user.id)
    await bot.send_message(message.from_user.id, '===== Главное меню =====', reply_markup=main_menu)
