from datetime import datetime
from bot import bot
from app.models import *
from bot.keyboards import gen_order_confirmed_buttons


def send_order(order_number: int):
    order = Order.get_or_none(order_number)
    products = OrderedProduct.select().where(OrderedProduct.order == order)
    time = datetime.strptime(order.time, '%Y-%m-%d %H:%M:%S%z')

    message = f'<b>Заказ №{order_number}</b>\n'
    message += f'<i>Содержание:</i>\n'

    for prod in products:
        message += f'  - {prod.product.product.name}, размер {prod.product.get_size_name()}'
        for top in ToppingToProduct.select().where(ToppingToProduct.ordered_product == prod):
            message += f' + {top.topping.name}'
        message += '\n'

    if order.comment:
        message += f'<i>Комментарий:</i> {order.comment}\n'

    message += f'<i>Приготовить к:</i> {time.strftime("%H:%M")}\n'
    message += f'<i>Имя покупателя:</i> {order.customer.name}\n'
    message += f'<i>Телефон покупателя:</i> +7{order.customer.phone_number}\n'

    bot.send_message(chat_id=order.coffee_house.chat_id, text=message, parse_mode='HTML',
                     reply_markup=gen_order_confirmed_buttons(order_number))


def send_login_code(login_code: LoginCode):
    msg = f'Код для входа: {login_code.code}'
    bot.send_message(chat_id=login_code.customer.chat_id, text=msg)
