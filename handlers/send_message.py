from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType
from keyboards import menu_callback, task_image_Menu, task_send_to_channel_menu, cancel_menu, back_to_main_menu
from keyboards.callback_datas import task_callback
from keyboards.task_menu import task_send_to_newsletter_menu
from loader import dp, bot, db, price_for_order, channel_id
from logic.clear_mesages import cleaner
from states import Task


# Начинаем создавать объявление
@dp.callback_query_handler(menu_callback.filter(btn='MESSAGE_announcement'))
@dp.callback_query_handler(menu_callback.filter(btn='MESSAGE_newsletter'))
async def enter_task(message: types.Message, callback_data: dict):
    state = dp.current_state(chat=message.from_user.id, user=message.from_user.id)
    await state.set_state(Task.task_type)
    async with state.proxy() as data:
        data['task_type'] = callback_data['btn']
    await cleaner.clear_bot_messages(message.from_user.id)
    await bot.delete_message(message.from_user.id, message.message.message_id)
    msg = await bot.send_message(message.from_user.id, Task.set_text_question, reply_markup=cancel_menu)
    cleaner.trash.append(msg.message_id)
    await Task.set_text.set()


# Текст объявления с выбором нужна ли картинка\фото
@dp.message_handler(state=Task.set_text)
async def set_text_message(message: types.Message, state: FSMContext):

    await cleaner.clear_bot_messages(message.chat.id)
    async with state.proxy() as data:
        data["set_text"] = message.text
    await bot.delete_message(message.chat.id, message.message_id)
    msg = await bot.send_message(message.from_user.id, Task.need_image_question, reply_markup=task_image_Menu)
    cleaner.trash.append(msg.message_id)


# Если фото\картинка не нужна
@dp.callback_query_handler(task_callback.filter(btn='MESSAGE_no_need_image'), state=Task.set_text)
async def no_need_image(message: types.Message, state: FSMContext):
    await cleaner.clear_bot_messages(message.from_user.id)
    async with state.proxy() as data:
        data["need_image"] = False
    result = await state.get_data()
    msg_preview = await bot.send_message(message.from_user.id, Task.check_before_send)
    if result['task_type'] == 'MESSAGE_announcement':
        menu = task_send_to_channel_menu
    else:
        menu = task_send_to_newsletter_menu
    msg_user = await bot.send_message(message.from_user.id, result['set_text'], reply_markup=menu)
    cleaner.trash.extend([msg_user.message_id, msg_preview.message_id])


# Если фото\картинка нужна
@dp.callback_query_handler(task_callback.filter(btn='MESSAGE_need_image'), state='*')
async def need_image(message: types.Message, state: FSMContext):
    await cleaner.clear_bot_messages(message.from_user.id)
    async with state.proxy() as data:
        data['need_image'] = True
    msg = await bot.send_message(message.from_user.id, Task.set_image_question)
    cleaner.trash.append(msg.message_id)
    await Task.set_image.set()


# Получаем картинку и формируем объявление с ней
@dp.message_handler(content_types=[ContentType.PHOTO], state=Task.set_image)
async def set_images(message: types.Message, state: FSMContext):
    await cleaner.clear_bot_messages(message.from_user.id)
    async with state.proxy() as data:
        data["set_image"] = message.photo[-1].file_id
    await bot.delete_message(message.chat.id, message.message_id)
    result = await state.get_data()
    msg_preview = await bot.send_message(message.from_user.id, Task.check_before_send)
    if result['task_type'] == 'MESSAGE_announcement':
        menu = task_send_to_channel_menu
    else:
        menu = task_send_to_newsletter_menu
    msg_user = await bot.send_photo(
        message.from_user.id,
        photo=result['set_image'],
        caption=result['set_text'],
        reply_markup=menu)
    cleaner.trash.extend([msg_user.message_id, msg_preview.message_id])


# Формирование объявление с\без картинки и отправка в канал
@dp.callback_query_handler(task_callback.filter(btn='MESSAGE_send_to_channel'), state='*')
@dp.callback_query_handler(task_callback.filter(btn='MESSAGE_send_to_newsletter'), state='*')
async def send_to_channel(message: types.Message, state: FSMContext, callback_data: dict):
    await cleaner.clear_bot_messages(message.from_user.id)
    result = await state.get_data()
    user_account = db.check_balance(message.from_user.id)
    if user_account > price_for_order:
        db.update_balance(message.from_user.id, -price_for_order)
        balance_now = db.check_balance(message.from_user.id)
        if callback_data['btn'] == 'MESSAGE_send_to_channel':
            if result['need_image']:
                await bot.send_photo(channel_id, photo=result["set_image"], caption=result['set_text'])
            else:
                await bot.send_message(channel_id, result['set_text'])
            text = 'Ваше сообщение отправлено в канал.'
        else:
            customers = db.get_random_people(10)
            if result['need_image']:
                for customer in customers:
                    print(customer)
                    # await bot.send_photo(customer, photo=result["set_image"], caption=result['set_text'])
            else:
                for customer in customers:
                    print(customer)
                    # await bot.send_message(channel_id, result['set_text'])
            text = 'Вашаш сообщение отправлено в рассылку.'
        msg_result = await bot.send_message(
            message.from_user.id,
            f'{text} Ваш текущий баланс <b>{balance_now} руб.</b>',
            reply_markup=back_to_main_menu)
        cleaner.trash.append(msg_result.message_id)
    else:
        balance_now = db.check_balance(message.from_user.id)
        msg_no_money = await bot.send_message(
            message.from_user.id,
            f'Недостаточно средств. Пополните Ваш баланс. Текущий баланс <b>{balance_now} руб.</b>',
            reply_markup=back_to_main_menu)
        await cleaner.clear_bot_messages(message.from_user.id)
        cleaner.trash.append(msg_no_money.message_id)
