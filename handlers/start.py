from aiogram import types
from aiogram.types import CallbackQuery

from keyboards import main_menu, admin_menu
from keyboards.callback_datas import task_callback, get_task_callback
from keyboards.task_menu import create_task_menu
from loader import dp, bot, db, admins
from logic.clear_mesages import cleaner


@dp.message_handler(commands=['start'])
async def role_menu(message: types.Message):

    if message.from_user.id in admins:
        menu = admin_menu
        menu_text = '===== Меню администратора ====='
    else:
        menu = main_menu
        menu_text = '===== Главное меню ====='
        msg = await bot.send_message(
            message.from_user.id,
            'Здравствуй {}! Бот находится в стадии разработки '
            'поэтому некоторый функционал сейчас недоступен. '
            'В данный момент мы ведём работу по подключению способа оплаты картой для пополнения счёта'
                .format(message.from_user['first_name']))
        cleaner.trash.append(msg.message_id)

    await bot.delete_message(message.chat.id, message.message_id)
    db.check_or_create_user(message.from_user.id, message.from_user.first_name, message.from_user.last_name)
    menu = await bot.send_message(message.from_user.id, menu_text, reply_markup=menu)
    cleaner.trash.append(menu.message_id)


# @dp.message_handler(commands=['test'])
# async def test(message: types.Message):
    # pic = db.get_task(12)
    # print(pic)
    # await bot.send_photo(message.from_user.id, pic)
