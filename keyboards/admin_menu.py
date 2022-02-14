from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards import admin_callback, menu_callback


# Главное админ меню
admin_menu = InlineKeyboardMarkup(row_width=1)

task_list_btn = InlineKeyboardButton(
    text='Список задач',
    callback_data=admin_callback.new(btn='ADMIN_task_list'))

contacts_import_btn = InlineKeyboardButton(
    text='Импорт контактов в базу',
    callback_data=admin_callback.new(btn='ADMIN_contacts_import'))

# to_main_menu_btn = InlineKeyboardButton(
#     text='В главное меню',
#     callback_data=menu_callback.new(btn='main_menu'))

admin_menu.insert(task_list_btn)
admin_menu.insert(contacts_import_btn)
# admin_menu.insert(to_main_menu_btn)


# Меню для отдельной задачи
admin_current_task_menu = InlineKeyboardMarkup(row_width=1)

in_progress_btn = InlineKeyboardButton(
    text='Взять в работу',
    callback_data=admin_callback.new(btn='ADMIN_in_progress'))

back_to_admin_menu_btn = InlineKeyboardButton(
    text='Назад в меню',
    callback_data=admin_callback.new(btn='back_to_admin_menu'))

admin_current_task_menu.insert(in_progress_btn)
admin_current_task_menu.insert(back_to_admin_menu_btn)


# Назад в админ меню
back_to_admin_menu = InlineKeyboardMarkup(row_width=1)
back_to_admin_menu.insert(back_to_admin_menu_btn)
