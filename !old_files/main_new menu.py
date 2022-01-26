from typing import List
from aiogram_media_group import MediaGroupFilter, media_group_handler
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types.input_media import InputMediaPhoto
from aiogram.types.message import ContentType
import keyboards as nav
from states import Task, Payment
from db import Database
import json

with open('../config.json') as conf:
    config = json.load(conf)
    TOKEN = config['token']
    test_payload_token = config['test_payment_id']
    channel_id = config["channel_id"]
    price_for_order = config["price_for_order"]
    price_for_comment = config["price_for_comment"]


# Инициализация бота
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML, )
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database()
task = Task()


async def clear_bot_messages(from_channel):
    try:
        if len(task.bot_last_message) > 0:
            for i in task.bot_last_message:
                await bot.delete_message(from_channel, i)
            task.bot_last_message.clear()
    except:
        print('Нечего удалять')



@dp.message_handler(commands='test')
async def test(message: types.message):
       msg = await message.answer('First message')
       await message.answer('Second message')
       await msg.delete()


@dp.message_handler(commands=['start'])
async def roleMenu(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)
    db.check_or_create_user(message.from_user.id, message.from_user.first_name, message.from_user.last_name)
    msg = await bot.send_message(
        message.from_user.id,
        'Здравствуй {}! бла бла бла какой нибудь текст'.format(message.from_user['first_name']))
    await bot.send_message(message.from_user.id, '===== Главное меню =====', reply_markup=nav.main_menu)
    task.bot_last_message.append(msg.message_id)

#   Главное меню
@dp.callback_query_handler(text='main_menu')
async def main_menu(message: types.Message, state: FSMContext):
    print('main_menu')
    await state.reset_state(with_data=True)
    await clear_bot_messages(message.from_user.id)
    await bot.send_message(message.from_user.id, '===== Главное меню =====', reply_markup=nav.main_menu)


# узнаём баланс
@dp.callback_query_handler(text='BALANCE_check_balance')
async def check_balance(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    balance = db.check_balance(message.from_user.id)
    msg = await bot.send_message(message.from_user.id, f'<b>Ваш баланс {balance} руб.</b>')
    print(task.bot_last_message)
    task.bot_last_message.append(msg.message_id)
    await bot.send_message(message.from_user.id, '=== Главное меню ===', reply_markup=nav.main_menu)


#  пополняем баланс
@dp.callback_query_handler(text='BALANCE_replenish_balance')
async def replenish_balance(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    msg = await bot.send_message(message.from_user.id, Payment.question1)
    task.bot_last_message.append(msg.message_id)
    await Payment.answer1.set()


@dp.message_handler(state=Payment.answer1)
async def send_invoice(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["answer1"] = message.text
    await state.finish()
    if int(data["answer1"]) > 99:
        msg = await bot.send_invoice(
            chat_id=message.chat.id,
            title="Пополнение счёта",
            description="test description",
            payload="test_payload",
            provider_token=test_payload_token,
            currency="RUB",
            start_parameter="test_bot",
            prices=[{"label": "Руб", "amount": int(data["answer1"]) * 100}]
        )
        menu = await bot.send_message(message.chat.id, 'вернуться в меню?', reply_markup=nav.to_main_menu)
        task.bot_last_message.extend([msg.message_id, menu.message_id])
    else:
        menu = await bot.send_message(message.chat.id, 'сумма меньше минимальной', reply_markup=nav.to_main_menu)
        task.bot_last_message.append(menu.message_id)


@dp.pre_checkout_query_handler()
async def pre_checkout(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_pay(message: types.Message):
    if message.successful_payment.invoice_payload == 'test_payload':
        db.update_balance(message.from_user.id, int(message.successful_payment["total_amount"] / 100))
        new_balance = db.check_balance(message.from_user.id)
        msg = await bot.send_message(message.from_user.id,
                                     f'Оплата прошла успешно!\n<b>Ваш баланс: {new_balance} руб.</b>',
                                     reply_markup=nav.to_main_menu)
        task.bot_last_message.append(msg.message_id)
        

# создаём объявление
@dp.callback_query_handler(text='CREATE_MESSAGE_enter_task')
async def enter_task(message: types.Message):
    await clear_bot_messages(message.from_user.id)
    await bot.delete_message(message.from_user.id, message.message.message_id)
    msg = await bot.send_message(message.from_user.id, task.set_text_question)
    task.bot_last_message.append(msg.message_id)
    await task.set_text.set()


@dp.message_handler(state=task.set_text)
async def set_text_message(message: types.Message, state: FSMContext):
    await clear_bot_messages(message.chat.id)
    async with state.proxy() as data:
        data["set_text"] = message.text
    await bot.delete_message(message.chat.id, message.message_id)
    msg = await bot.send_message(message.from_user.id, task.need_image_question, reply_markup=nav.taskMenu)
    task.bot_last_message.append(msg.message_id)


@dp.callback_query_handler(text='CREATE_MESSAGE_no_need_image', state=task.set_text)
async def no_need_image(message: types.Message, state: FSMContext):
    await clear_bot_messages(message.from_user.id)
    async with state.proxy() as data:
        data["need_image"] = False
    result = await state.get_data()
    msg_preview = await bot.send_message(message.from_user.id, 'Вот твоё сообщение, проверь перед отправкой')
    msg_user = await bot.send_message(message.from_user.id, result['set_text'])
    task.bot_last_message.extend([msg_user.message_id, msg_preview.message_id])
    await bot.send_message(message.from_user.id, 'Куда отправить объявление?', reply_markup=nav.task_choise_menu)
    await task.choise.set()


@dp.callback_query_handler(text='CREATE_MESSAGE_need_image', state=Task.set_text)
async def need_image(message: types.Message, state: FSMContext):
    await clear_bot_messages(message.from_user.id)
    async with state.proxy() as data:
        data['need_image'] = True
        data["set_image"] = []
    msg = await bot.send_message(message.from_user.id, task.set_image_question)
    task.bot_last_message.append(msg.message_id)
    await task.set_image.set()


@dp.message_handler(MediaGroupFilter(), content_types=[ContentType.PHOTO], state=task.set_image)
@media_group_handler
async def set_images(messages: List[types.Message], state: FSMContext):
    await clear_bot_messages(messages[0].from_user.id)
    result = await state.get_data()
    for message in messages:
        if messages.index(message) == 0:
            async with state.proxy() as data:
                data["set_image"].append(InputMediaPhoto(message.photo[-1].file_id, result['set_text']))
        else:
            async with state.proxy() as data:
                data["set_image"].append(InputMediaPhoto(message.photo[-1].file_id))
        await bot.delete_message(message.chat.id, message.message_id)
    msg_preview = await bot.send_message(message.from_user.id, 'Вот твоё сообщение, проверь перед отправкой')
    msg_media = await bot.send_media_group(messages[0].from_user.id, data["set_image"])
    await bot.send_message(message.from_user.id, 'Куда отправить объявление?', reply_markup=nav.task_choise_menu)
    for i in msg_media:
        task.bot_last_message.append(i.message_id)
    task.bot_last_message.append(msg_preview.message_id)
    await task.choise.set()


@dp.callback_query_handler(text_contains='CREATE_MESSAGE_choise', state=task.choise)
async def task_choise(call: types.Message, state: FSMContext):
    await clear_bot_messages(call.from_user.id)
    await bot.delete_message(call.from_user.id, call.message.message_id)

    # Отправляем объявление в канал
    if call.data == 'CREATE_MESSAGE_choiseChannel':
        result = await state.get_data()
        user_account = db.check_balance(call.from_user.id)
        if user_account > price_for_order:
            db.update_balance(call.from_user.id, -price_for_order)
            balance_now = db.check_balance(call.from_user.id)
            if result['need_image']:
                await bot.send_media_group(channel_id, result["set_image"])
            else:
                await bot.send_message(channel_id, result['set_text'])
            msg_result = await bot.send_message(
                call.from_user.id,
                f'Сообщение отправлено в наш канал. Ваш текущий баланс <b>{balance_now} руб.</b>',
                reply_markup=nav.to_main_menu)
            # await clear_bot_messages(call.from_user.id)
            task.bot_last_message.append(msg_result.message_id)
        else:
            balance_now = db.check_balance(call.from_user.id)
            msg_no_money = await bot.send_message(
                call.from_user.id,
                f'Недостаточно средств. Пополните Ваш баланс. Текущий баланс <b>{balance_now} руб.</b>',
                reply_markup=nav.to_main_menu)
            await clear_bot_messages(call.from_user.id)
            task.bot_last_message.append(msg_no_money.message_id)

    # Отправляем объявление в рассылку
    elif call.data == 'choiseNewsletter':
        pass

    await state.finish()

executor.start_polling(dp, skip_updates=True)
