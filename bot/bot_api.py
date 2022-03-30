from fastapi import APIRouter
import telebot

from app.models import Order
from backend.settings import DOMAIN, SERVER_PORT, API_TOKEN
from bot import bot
from bot.email_sender import send_email

router = APIRouter()


def set_webhook():
    webhook_url = f"https://{DOMAIN}:{SERVER_PORT}" + f'/{API_TOKEN}/'
    if bot.get_webhook_info().url != webhook_url:
        bot.remove_webhook()
        bot.set_webhook(url=webhook_url)


@router.post(f'/{API_TOKEN}/')
def process_webhook(update: dict):
    if update:
        update = telebot.types.Update.de_json(update)
        bot.process_new_updates([update])
    else:
        return


@bot.message_handler(commands=['start'])
def send_welcome(message):
    print(message.chat.id)
    bot.reply_to(message, f"Hello, i'm coffefu webhook bot. Chat {message.chat.id}")


@bot.callback_query_handler(func=lambda call: True)
def callback_processing(call):
    cb_ans, order_number = call.data.split()
    ans = 'Заказ принят' if cb_ans == 'yes' else 'Заказ отклонен'
    bot.answer_callback_query(call.id, ans)
    ans = f"\n<b>{ans}</b>"

    order = Order.get_or_none(id=int(order_number))
    status = (cb_ans == 'yes')
    order.status = status

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=call.message.text + ans, parse_mode='HTML', reply_markup=None)

    if order.customer.email:
        customer_email = order.customer.email
        send_email(customer_email, int(order_number), status)