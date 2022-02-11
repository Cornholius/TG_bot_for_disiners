from aiogram.utils.callback_data import CallbackData

menu_callback = CallbackData('menu', 'btn')
message_callback = CallbackData('msg', 'btn')
task_callback = CallbackData('task', 'btn')
get_task_callback = CallbackData('get_task', 'btn', 'task_id')
designer_callback = CallbackData('designer', 'btn')
