from aiogram import executor
# from loader import dp
from handlers import dp

executor.start_polling(dp, skip_updates=True)
