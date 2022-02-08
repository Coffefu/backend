import telebot
from telebot import types


def send_order(order: dict, bot: telebot.TeleBot):
    message = f'<b>Заказ №{order["order_number"]}</b>\n'
    message += f'<i>Содержание:</i> {order["product_name"]}\n'
    message += f'<i>Приготовить к:</i> {order["time"].strftime("%H:%M")}\n'
    message += f'<i>Имя покупателя:</i> {order["customer_name"]}\n'
    if 'phone_number' in order:
        message += f'<i>Телефон покупателя:</i> +7{order["phone_number"]}\n'
    if 'email' in order:
        message += f'<i>Почта покупателя:</i> {order["email"]}\n'

    bot.send_message(chat_id=order["coffee_house_chat_id"], text=message, parse_mode='HTML', reply_markup=markup_btns)


markup_btns = types.InlineKeyboardMarkup(row_width=2)
markup_btns.add(
    types.InlineKeyboardButton('Принять', callback_data='cb_yes'),
    types.InlineKeyboardButton('Отклонить', callback_data='cb_no')
)

