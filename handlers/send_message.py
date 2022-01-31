from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from logic.clear_mesages import clear_bot_messages
from states import Task


@dp.callback_query_handler(text='CREATE_MESSAGE_enter_task')
async def enter_task(message: types.Message):
    await clear_bot_messages(message.from_user.id)
    await bot.delete_message(message.from_user.id, message.message.message_id)
    msg = await bot.send_message(message.from_user.id, Task.set_text_question)
    Task.bot_last_message.append(msg.message_id)
    await Task.set_text.set()


@dp.message_handler(state=Task.set_text)
async def set_text_message(message: types.Message, state: FSMContext):
    await clear_bot_messages(message.chat.id)
    async with state.proxy() as data:
        data["set_text"] = message.text
    await bot.delete_message(message.chat.id, message.message_id)
    msg = await bot.send_message(message.from_user.id, Task.need_image_question, reply_markup=nav.taskMenu)
    Task.bot_last_message.append(msg.message_id)
