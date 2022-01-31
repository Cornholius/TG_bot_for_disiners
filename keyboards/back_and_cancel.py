from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.callback_datas import menu_callback


# Кнопка возврата в главное меню
back_to_main_menu = InlineKeyboardMarkup(row_width=1)
back_to_main_menu_btn = InlineKeyboardButton(
    text='Вернуться в главное меню',
    callback_data=menu_callback.new(btn='main_menu'))
back_to_main_menu.insert(back_to_main_menu_btn)

# Кнопка отмены
cancel_menu = InlineKeyboardMarkup(row_width=1)
cancel_menu_btn = InlineKeyboardButton(
    text='Отмена',
    callback_data=menu_callback.new(btn='main_menu'))
cancel_menu.insert(cancel_menu_btn)
