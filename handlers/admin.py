import re
from aiogram import types
from aiogram.types import ContentType, CallbackQuery

from keyboards import get_task_callback
from keyboards.task_menu import create_task_menu
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


@dp.message_handler(commands=['gettask'])
async def get_task(message: types.Message):
    for task in db.get_all_tasks():
        text = f'Заявка №{task[0]}\nЗаказчик: {task[1]}\nСтатус {task[5]}'
        msg = await message.answer(text, reply_markup=create_task_menu(task[0]))
        cleaner.trash.append(msg.message_id)


@dp.callback_query_handler(get_task_callback.filter(btn='TASK_get_task'))
async def send_task_to_email(call: CallbackQuery, callback_data: dict):
    print(callback_data['task_id'])
    task = db.get_current_task(callback_data['task_id'])
    print(task)
    text = f'заказчик: {task[1]}\n\nтекст рассылки:\n{task[2]}\n\nid для рассылки:\n{task[4]}'
    await call.message.answer(text)
