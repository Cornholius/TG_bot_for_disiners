from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.callback_datas import menu_callback


# Кноапка возврата в главное меню
back_to_main_menu = InlineKeyboardMarkup(row_width=1)
back_to_main_menu_btn = InlineKeyboardButton(
    text='Вернуться в главное меню',
    callback_data=menu_callback.new(btn='main_menu'))
back_to_main_menu.insert(back_to_main_menu_btn)
