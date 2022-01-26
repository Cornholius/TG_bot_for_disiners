from aiogram.types import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

need_image_btn = KeyboardButton(text='Да', callback_data='CREATE_MESSAGE_need_image')
no_need_image_btn = KeyboardButton(text='Нет', callback_data='CREATE_MESSAGE_no_need_image')
in_channel_btn = InlineKeyboardButton(text='В канал', callback_data='CREATE_MESSAGE_choiseChannel')
in_newsletter_btn = InlineKeyboardButton(text='В рассылку', callback_data='CREATE_MESSAGE_choiseNewsletter')
to_main_menu_btn = InlineKeyboardButton(text='Вернуться в главное меню', callback_data='main_menu')
image_complete_btn = InlineKeyboardButton(text='Готово, поехали дальше', callback_data='ololo2')

taskMenu = InlineKeyboardMarkup(row_width=2)
task_choise_menu = InlineKeyboardMarkup(row_width=1)
image_complete = InlineKeyboardMarkup(row_width=1)

taskMenu.insert(need_image_btn)
taskMenu.insert(no_need_image_btn)
taskMenu.insert(to_main_menu_btn)

task_choise_menu.insert(in_channel_btn)
task_choise_menu.insert(in_newsletter_btn)

image_complete.insert(image_complete_btn)