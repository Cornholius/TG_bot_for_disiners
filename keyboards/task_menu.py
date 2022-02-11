from aiogram.types import KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.back_and_cancel import cancel_menu_btn, back_to_main_menu_btn
from keyboards.callback_datas import task_callback, get_task_callback

need_image_btn = KeyboardButton(
    text='Да',
    callback_data=task_callback.new('MESSAGE_need_image'))
no_need_image_btn = KeyboardButton(
    text='Нет',
    callback_data=task_callback.new('MESSAGE_no_need_image'))
send_to_channel_btn = KeyboardButton(
    text='Отправить в канал',
    callback_data=task_callback.new('MESSAGE_send_to_channel'))

send_to_newsletter_btn = KeyboardButton(
    text='Отправить в рассылку',
    callback_data=task_callback.new('MESSAGE_send_to_newsletter'))

task_image_Menu = InlineKeyboardMarkup(row_width=2)
task_send_to_channel_menu = InlineKeyboardMarkup(row_width=1)
task_send_to_newsletter_menu = InlineKeyboardMarkup(row_width=1)

task_image_Menu.insert(need_image_btn)
task_image_Menu.insert(no_need_image_btn)
task_image_Menu.insert(cancel_menu_btn)

task_send_to_channel_menu.insert(send_to_channel_btn)
task_send_to_channel_menu.insert(back_to_main_menu_btn)
task_send_to_newsletter_menu.insert(send_to_newsletter_btn)
task_send_to_newsletter_menu.insert(back_to_main_menu_btn)


# Меню для получения задачи на почту
# get_task_menu = InlineKeyboardMarkup(row_width=1)
# get_task_menu_btn = KeyboardButton(
#     text='Взять задачу',
#     callback_data=get_task_callback.new(btn='TASK_get_task', task_id='098'))
# get_task_menu.insert(get_task_menu_btn)

def create_task_menu(task_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [KeyboardButton(text='Взять задачу', callback_data=get_task_callback.new(btn='TASK_get_task', task_id=task_id))]
        ])