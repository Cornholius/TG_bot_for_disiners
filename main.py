from aiogram import Bot, Dispatcher, executor, types
import markups as nav
import json

with open('config.json') as conf:
    config = json.load(conf)
    TOKEN = config['token']

# Инициализация бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def roleMenu(message: types.Message):
    await bot.send_message(
        message.from_user.id, 
        'Здравствуй {}! Ты заказчик или дизайнер?'.format(message.from_user['first_name']), 
        reply_markup=nav.roleMenu)










executor.start_polling(dp, skip_updates=True)