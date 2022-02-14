import re
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType, CallbackQuery
from filters import IsAdmin
from keyboards import get_task_callback, admin_callback, admin_current_task_menu, admin_menu, main_menu, back_to_admin_menu
from keyboards.task_menu import create_task_menu, current_task_menu
from loader import dp, bot, db
from logic.clear_mesages import cleaner
import urllib.request


# Импортируем список контактов в базу
from states import ImportContacts


@dp.callback_query_handler(IsAdmin(), admin_callback.filter(btn='ADMIN_contacts_import'))
async def import_contacts(call: types.CallbackQuery):
    await cleaner.clear_bot_messages(call.from_user.id)
    msg = await call.message.answer(
        "Загрузи *.txt файл в котором будут находиться id контактов."
        "Каждый id должен начинаться с новой строки",
        reply_markup=back_to_admin_menu
    )
    cleaner.trash.append(msg.message_id)
    await ImportContacts.set_doc.set()


@dp.message_handler(IsAdmin(), content_types=[ContentType.DOCUMENT], state=ImportContacts.set_doc)
async def catch_doc(message: types.Message, state: FSMContext):
    await cleaner.clear_bot_messages(message.from_user.id)
    url = await message.document.get_url()
    doc = urllib.request.urlopen(url)
    count = 0
    for i in doc.readlines():
        try:
            i.isdigit()
            # user_id = re.sub("[^0-9]", "", str(i))
            db.add_customer(int(i))
            count += 1
        except:
            print(re.sub("[^0-9]", "", str(i)))
    await bot.delete_message(message.chat.id, message.message_id)
    msg = await bot.send_message(message.from_user.id, f'Добавлено {count} записей.')
    cleaner.trash.append(msg.message_id)
    msg2 = await bot.send_message(message.from_user.id, '===== Меню администратора =====', reply_markup=admin_menu)
    cleaner.trash.append(msg2.message_id)
    await state.finish()


# Получаем список задач на рассылку
@dp.callback_query_handler(admin_callback.filter(btn='ADMIN_task_list'))
async def task_list(call: CallbackQuery):
    await cleaner.clear_bot_messages(call.from_user.id)
    # menu = await bot.delete_message(call.from_user.id, call.message.message_id)
    if len(db.get_all_tasks()) == 0:
        msg = await bot.send_message(call.from_user.id, 'Активных задач нет')
        msg2 = await bot.send_message(call.from_user.id, '===== Меню администратора =====', reply_markup=admin_menu)
        messages = [msg.message_id, msg2.message_id]
        cleaner.trash.extend(messages)
    else:
        for task in db.get_all_tasks():
            text = f'Заявка №{task[0]}\nЗаказчик: {task[1]}\nСтатус {task[5]}'
            msg = await call.message.answer(text, reply_markup=create_task_menu(task[0]))
            cleaner.trash.append(msg.message_id)


# Переход внутрь выбранной задачи
@dp.callback_query_handler(get_task_callback.filter(btn='TASK_get_task'))
async def get_task(call: CallbackQuery, callback_data: dict):
    await cleaner.clear_bot_messages(call.from_user.id)
    task = db.get_current_task(callback_data['task_id'])
    text = f'СТАТУС: {task[5]}\n\nзаказчик: {task[1]}\n\nтекст рассылки:\n{task[2]}\n\nid для рассылки:\n{task[4]}'
    msg = await call.message.answer(text, reply_markup=current_task_menu(task[0]))
    cleaner.trash.append(msg.message_id)


# Обновление статуса задачи на "IN WORK"/"NEW"
@dp.callback_query_handler(get_task_callback.filter(btn=['TASK_status_IN_WORK', 'TASK_status_NEW']))
async def task_status_in_work(call: CallbackQuery, callback_data: dict):

    if callback_data['btn'] == 'TASK_status_IN_WORK':
        db.change_status_task(callback_data['task_id'], 'IN WORK')
    elif callback_data['btn'] == 'TASK_status_NEW':
        db.change_status_task(callback_data['task_id'], 'NEW')

    await call.message.delete()
    task = db.get_current_task(callback_data['task_id'])
    text = f'СТАТУС: {task[5]}\n\nзаказчик: {task[1]}\n\nтекст рассылки:\n{task[2]}\n\nid для рассылки:\n{task[4]}'
    await bot.send_message(call.from_user.id, text, reply_markup=current_task_menu(task[0]))


# Удаление задачи при её выполнении
@dp.callback_query_handler(get_task_callback.filter(btn='TASK_done'))
async def task_done(call: CallbackQuery, callback_data: dict):
    db.delete_task(callback_data['task_id'])
    await call.message.delete()
    await bot.send_message(call.from_user.id, '===== Меню администратора =====', reply_markup=admin_menu)
