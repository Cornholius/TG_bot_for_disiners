import re
from aiogram import types
from aiogram.types import ContentType
from loader import dp, bot, db
from logic.clear_mesages import cleaner
import urllib.request


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
