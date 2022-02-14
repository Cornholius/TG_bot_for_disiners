from aiogram import executor
from loader import dp
import filters, handlers

executor.start_polling(dp, skip_updates=True)
