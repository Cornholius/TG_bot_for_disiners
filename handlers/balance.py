from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ContentType
from keyboards import back_to_main_menu, cancel_menu, menu_callback
from loader import dp, bot, db, test_payload_token
from logic.clear_mesages import cleaner
from states import Payment


# узнаём баланс
@dp.callback_query_handler(menu_callback.filter(btn='BALANCE_check_balance'))
async def check_balance(call: CallbackQuery):
    balance = db.check_balance(call.from_user.id)
    await call.answer(f'Ваш баланс {balance} руб.', show_alert=True)


#  пополняем баланс
@dp.callback_query_handler(menu_callback.filter(btn='BALANCE_replenish_balance'))
async def replenish_balance(call: types.CallbackQuery):
    await cleaner.clear_bot_messages(call.from_user.id)
    # await bot.delete_message(call.from_user.id, call.message.message_id)
    msg = await bot.send_message(call.from_user.id, Payment.question1, reply_markup=cancel_menu)
    cleaner.trash.append(msg.message_id)
    await Payment.answer1.set()


@dp.message_handler(state=Payment.answer1)
async def send_invoice(message: types.Message, state: FSMContext):
    await cleaner.clear_bot_messages(message.from_user.id)
    await bot.delete_message(message.from_user.id, message.message_id)
    if message.text.isdigit() and int(message.text) > 99:
        async with state.proxy() as data:
            data["answer1"] = message.text
        await state.finish()
        msg = await bot.send_invoice(
            chat_id=message.chat.id,
            title="Пополнение счёта",
            description="test description",
            payload="test_payload",
            provider_token=test_payload_token,
            currency="RUB",
            start_parameter="test_bot",
            prices=[{"label": "Руб", "amount": int(data["answer1"]) * 100}]
        )
        msg2 = await bot.send_message(message.chat.id, '===== Главное меню =====', reply_markup=back_to_main_menu)
        cleaner.trash.extend([msg.message_id, msg2.message_id])
    elif message.text.isdigit() and int(message.text) < 100:
        menu = await bot.send_message(message.chat.id, 'сумма меньше минимальной, давай ещё раз')
        cleaner.trash.append(menu.message_id)
        await Payment.answer1.set()
    else:
        menu = await bot.send_message(message.chat.id, 'только целые числа, давай ещё')
        cleaner.trash.append(menu.message_id)
        await Payment.answer1.set()


@dp.pre_checkout_query_handler()
async def pre_checkout(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_pay(message: types.Message):
    await cleaner.clear_bot_messages(message.from_user.id)
    if message.successful_payment.invoice_payload == 'test_payload':
        db.update_balance(message.from_user.id, int(message.successful_payment["total_amount"] / 100))
        new_balance = db.check_balance(message.from_user.id)
        msg = await bot.send_message(message.from_user.id,
                                     f'Оплата прошла успешно!\n<b>Ваш баланс: {new_balance} руб.</b>',
                                     reply_markup=back_to_main_menu)
        cleaner.trash.append(msg.message_id)

