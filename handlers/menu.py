from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards import main_menu
from keyboards.callback_datas import menu_callback
from loader import dp, bot
from logic.clear_mesages import cleaner


@dp.callback_query_handler(menu_callback.filter(btn='main_menu'), state='*')
async def to_main_menu(message: types.Message, state: FSMContext):
    await state.finish()
    await cleaner.clear_bot_messages(message.from_user.id)
    await bot.send_message(message.from_user.id, '===== Главное меню =====', reply_markup=main_menu)
