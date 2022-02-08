from aiogram import types
from keyboards import main_menu
from loader import dp, bot, db
from logic.clear_mesages import cleaner


@dp.message_handler(commands=['start'])
async def role_menu(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)
    db.check_or_create_user(message.from_user.id, message.from_user.first_name, message.from_user.last_name)
    msg = await bot.send_message(
        message.from_user.id,
        'Здравствуй {}! бла бла бла какой нибудь текст'.format(message.from_user['first_name']))
    await bot.send_message(message.from_user.id, '===== Главное меню =====', reply_markup=main_menu)
    cleaner.trash.append(msg.message_id)
