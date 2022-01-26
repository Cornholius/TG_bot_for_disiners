from loader import bot
from states import Task


async def clear_bot_messages(from_channel):
    try:
        if len(Task.bot_last_message) > 0:
            for i in Task.bot_last_message:
                await bot.delete_message(from_channel, i)
            Task.bot_last_message.clear()
    except:
        print('Нечего удалять')
