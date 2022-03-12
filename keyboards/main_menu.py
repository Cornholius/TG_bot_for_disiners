from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards import menu_callback

# callback_data=menu_callback.new(btn='main_menu')

check_money_btn = InlineKeyboardButton(
    text='Узнать баланс',
    callback_data=menu_callback.new(btn='BALANCE_check_balance'))

give_money_btn = InlineKeyboardButton(
    text='Пополнить баланс',
    callback_data=menu_callback.new(btn='BALANCE_replenish_balance'))

make_announcement_btn = InlineKeyboardButton(
    text='Разместить объявление',
    callback_data=menu_callback.new(btn='MESSAGE_announcement'))

make_newsletter_btn = InlineKeyboardButton(
    text='Сделать рассылку',
    callback_data=menu_callback.new(btn='MESSAGE_newsletter'))

rtfm_btn = InlineKeyboardButton(
    text='Помощь',
    callback_data=menu_callback.new(btn='rtfm'))

prices_btn = InlineKeyboardButton(
    text='Прайс лист',
    callback_data=menu_callback.new(btn='prices'))

about_us_btn = InlineKeyboardButton(
    text='О нас',
    callback_data=menu_callback.new(btn='about_us'))


main_menu = InlineKeyboardMarkup(row_width=2)

main_menu.insert(check_money_btn)
main_menu.insert(give_money_btn)
main_menu.insert(make_announcement_btn)
main_menu.insert(make_newsletter_btn)
main_menu.insert(prices_btn)
main_menu.insert(rtfm_btn)
main_menu.insert(about_us_btn)
