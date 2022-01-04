from types import new_class
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import message_id
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types.message import ContentType, Message
import markups as nav
from states import Task, Payment
from db import Database
import json


with open('config.json') as conf:
    config = json.load(conf)
    TOKEN = config['token']
    test_payload_token = config['test_payment_id']


# Инициализация бота
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database()

@dp.pre_checkout_query_handler()
async def pre_checkout(pre_checkout_query: types.PreCheckoutQuery):
    print(pre_checkout_query)
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_pay(message: types.Message):
    print(message['total_amount'])
    if message.successful_payment.invoice_payload == 'test_payload':
        await bot.send_message(message.from_user.id, 'Оплата прошла успешно!')
        
@dp.message_handler(commands=['start'])
async def roleMenu(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)
    db.check_or_create_user(message.from_user.id)
    await bot.send_message(
        message.from_user.id, 
        'Здравствуй {}! Ты заказчик или дизайнер?'.format(message.from_user['first_name']), 
        reply_markup=nav.roleMenu)


@dp.callback_query_handler(text='mainMenuCustomer')
async def mainMenuCustomer(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    description = 'Добро пожаловать! Я помогу Вам найти исполнителя, просто разместите свое объявление. Стоимость составляет {price} руб.'
    await bot.send_message(message.from_user.id, description, reply_markup=nav.customerMenu)





# узнаём баланс
async def check_balance(message: types.Message):
        await bot.delete_message(message.chat.id, message.message_id)
        balance = db.check_balance(message.from_user.id)
        await bot.send_message(message.from_user.id, f'<b>Ваш баланс {balance} руб.</b>')


#  пополняем баланс
async def replenish_balance(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)
    await bot.send_message(message.from_user.id, Payment.question1)
    await Payment.answer1.set()


@dp.message_handler(state=Payment.answer1)
async def send_invoice(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["answer1"] = message.text
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
    print('>>>>> Send invoice')


# размещаем объявление
async def enter_task(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)
    await bot.send_message(message.from_user.id, Task.question1)
    await Task.answer1.set()

@dp.message_handler(state=Task.answer1)
async def answer_1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["answer1"] = message.text
    await message.answer(Task.question2)
    await Task.next()

@dp.message_handler(state=Task.answer2)
async def answer_2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["answer2"] = message.text
    await message.answer(Task.question3)
    await Task.next()

@dp.message_handler(state=Task.answer3)
async def answer_3(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["answer3"] = message.text
    result = await state.get_data()
    task_message = '''
    {}\n
    Сумма вознаграждения: <b>{}</b> 
    '''.format(result['answer2'], result['answer3'])
    await bot.send_message(message.from_user.id, Task.task_complete)
    await bot.send_message(-1001773059385, task_message)
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