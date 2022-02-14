from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards import main_menu, admin_menu
from keyboards.callback_datas import menu_callback, admin_callback
from loader import dp, bot
from logic.clear_mesages import cleaner


@dp.callback_query_handler(menu_callback.filter(btn='main_menu'), state='*')
async def to_main_menu(message: types.Message, state: FSMContext):
    await state.finish()
    await cleaner.clear_bot_messages(message.from_user.id)
    msg = await bot.send_message(message.from_user.id, '===== Главное меню =====', reply_markup=main_menu)
    cleaner.trash.append(msg.message_id)


@dp.callback_query_handler(admin_callback.filter(btn='back_to_admin_menu'), state='*')
async def to_admin_menu(message: types.Message, state: FSMContext):
    await state.finish()
    await cleaner.clear_bot_messages(message.from_user.id)
    msg = await bot.send_message(message.from_user.id, '===== Меню администратора =====', reply_markup=admin_menu)
    cleaner.trash.append(msg.message_id)

