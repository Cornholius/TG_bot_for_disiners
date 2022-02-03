import re

from aiogram import types
from aiogram.types import ContentType

from keyboards import main_menu
from loader import dp, bot, db
from logic.clear_mesages import cleaner
from states import Task
import urllib.request


@dp.message_handler(commands=['start'])
async def role_menu(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)
    db.check_or_create_user(message.from_user.id, message.from_user.first_name, message.from_user.last_name)
    msg = await bot.send_message(
        message.from_user.id,
        'Здравствуй {}! бла бла бла какой нибудь текст'.format(message.from_user['first_name']))
    await bot.send_message(message.from_user.id, '===== Главное меню =====', reply_markup=main_menu)
    cleaner.trash.append(msg.message_id)


@dp.message_handler(content_types=[ContentType.DOCUMENT])
async def catch_doc(message: types.Message):
    url = await message.document.get_url()
    doc = urllib.request.urlopen(url)
    count = 0
    for i in doc.readlines():
        try:
            user_id = re.sub("[^0-9]", "", str(i))
            db.add_customer(int(user_id))
            count += 1
        except:
            print(re.sub("[^0-9]", "", str(i)))
    await bot.delete_message(message.chat.id, message.message_id)
    msg = await bot.send_message(message.from_user.id, f'Добавлено {count} записей.')
    cleaner.trash.append(msg.message_id)
