from loader import bot
from states import Task


class Cleaner:

    trash = []

    async def clear_bot_messages(self, from_channel):
        try:
            if len(self.trash) > 0:
                for i in self.trash:
                    await bot.delete_message(from_channel, i)
                self.trash.clear()
        except:
            print('Нечего удалять')


cleaner = Cleaner()
