from aiogram.types import KeyboardButton, InlineKeyboardMarkup
from keyboards.callback_datas import designer_callback

to_chat_with_designer = KeyboardButton(
    text='Написать дизайнеру',
    callback_data=designer_callback.new('DESIGNER_chat'))


designer_contact = InlineKeyboardMarkup()
designer_contact.insert(to_chat_with_designer)
