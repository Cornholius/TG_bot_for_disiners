from typing import List
from aiogram_media_group import MediaGroupFilter, media_group_handler
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types.input_media import InputMediaPhoto
from aiogram.types.message import ContentType
import markups as nav
from states import Task, Payment
from db import Database
import json


with open('config.json') as conf:
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


@dp.message_handler(commands=['start'])
async def roleMenu(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)
    db.check_or_create_user(message.from_user.id, message.from_user.first_name, message.from_user.last_name)
    await bot.send_message(
        message.from_user.id, 
        'Здравствуй {}! бла бла бла какой нибудь текст'.format(message.from_user['first_name']),
        reply_markup=nav.customerMenu)


# @dp.callback_query_handler(text='mainMenuCustomer')
# async def mainMenuCustomer(message: types.Message):
#     await bot.delete_message(message.from_user.id, message.message.message_id)
#     description = 'Добро пожаловать! Я помогу Вам найти исполнителя, просто разместите свое объявление. ' \
#                   'Стоимость составляет {price} руб.'
#     await bot.send_message(message.from_user.id, description, reply_markup=nav.customerMenu)


# # узнаём баланс
async def check_balance(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)
    balance = db.check_balance(message.from_user.id)
    await bot.send_message(message.from_user.id, f'<b>Ваш баланс {balance} руб.</b>', show_alert=True)
    # await bot.answer_callback_query(message.from_user.id, f'<b>Ваш баланс {balance} руб.</b>', show_alert=True)


#  пополняем баланс
async def replenish_balance(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)
    await bot.send_message(message.from_user.id, Payment.question1)
    await Payment.answer1.set()


@dp.message_handler(state=Payment.answer1)
async def send_invoice(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["answer1"] = message.text
    await state.finish()
    await bot.send_invoice(
        chat_id=message.chat.id,
        title="Пополнение счёта",
        description="test description",
        payload="test_payload",
        provider_token=test_payload_token,
        currency="RUB",
        start_parameter="test_bot",
        prices=[{"label": "Руб", "amount": int(data["answer1"]) * 100}]
    )


@dp.pre_checkout_query_handler()
async def pre_checkout(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_pay(message: types.Message):
    if message.successful_payment.invoice_payload == 'test_payload':
        db.update_balance(message.from_user.id, int(message.successful_payment["total_amount"] / 100))
        new_balance = db.check_balance(message.from_user.id)
        await bot.send_message(message.from_user.id, f'Оплата прошла успешно!\n<b>Ваш баланс: {new_balance} руб.</b>')
        

# создаём объявление
async def enter_task(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)
    if db.check_balance(message.from_user.id) > price_for_order:
        await bot.send_message(message.from_user.id, Task.set_text_question)
        await Task.set_text.set()
    else:
        await bot.send_message(message.from_user.id, f"У вас недостаточно средств на балансе. Ваш баланс "
                                                     f"<b>{db.check_balance(message.from_user.id)}</b> руб.")


@dp.message_handler(state=Task.set_text)
async def set_text_message(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["set_text"] = message.text
    await message.answer(Task.set_image_question)
    await Task.next()


@dp.message_handler(MediaGroupFilter(), content_types=ContentType.PHOTO, state=Task.set_image)
@media_group_handler
async def set_images(messages: List[types.Message], state: FSMContext):
    result = await state.get_data()
    images = []
    for message in messages:
        if messages.index(message) == 0:
            images.append(InputMediaPhoto(message.photo[-1].file_id, result['set_text']))
        else:
            images.append(InputMediaPhoto(message.photo[-1].file_id))
    await bot.send_media_group(message.from_user.id, images)
    await state.finish()


# главное меню
@dp.message_handler()
async def mainMenu(message: types.Message):
    if message.text == 'Узнать баланс':
        await check_balance(message)
    elif message.text == 'Пополнить баланс':
        await replenish_balance(message)
    elif message.text == 'Разместить объявление':
        await enter_task(message)
    
executor.start_polling(dp, skip_updates=True)
