from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from loader import admins


class IsAdmin(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        if message.from_user.id in admins:
            return True
        else:
            return False
