from aiogram import executor
from handlers import dp

executor.start_polling(dp, skip_updates=True)
