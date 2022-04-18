from fastapi import APIRouter
import telebot

from app.models import Order, Customer, CoffeeHouse
from backend.settings import DOMAIN, BOT_TOKEN, BOT_PORT
from bot import bot
from telebot import types
from bot.email_sender import send_email

router = APIRouter()


def gen_send_contact_markup():
    btn = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn.add(
        types.KeyboardButton('Подтвердить номер телефона', request_contact=True)
    )
    return btn


def set_webhook():
    webhook_url = f"https://{DOMAIN}:{BOT_PORT}" + f'/bot/{BOT_TOKEN}/'
    if bot.get_webhook_info().url != webhook_url:
        bot.remove_webhook()
        bot.set_webhook(url=webhook_url)


@router.post(f'/{BOT_TOKEN}/', include_in_schema=False)
def process_webhook(update: dict):
    if update:
        update = telebot.types.Update.de_json(update)
        bot.process_new_updates([update])
    else:
        return


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = gen_send_contact_markup()
    if message.chat.type == 'group':
        markup = None
    bot.send_message(message.chat.id,
                     f"Hello, i'm cofefu webhook bot.",
                     reply_markup=markup)


@bot.message_handler(commands=['help'])
def send_help_info(message):
    msg = 'Команды:\n'
    if message.chat.type == 'group':
        msg += '<b>/status</b> НОМЕР_ЗАКАЗА - чтобы узнать статус указанного заказа'
    else:
        msg += '<b>/start</b> - для подтверждения номера телефона'
    msg += '<b>/bug_report</b> ТЕКСТ - для информации о различных ошибках'
    msg += '<b>/feed_back</b> ТЕКСТ - для советов, пожеланий'

    bot.send_message(chat_id=message.chat.id, text=msg, parse_mode='HTML')


@bot.message_handler(commands=['chat_id'])
def send_chat_id(message):
    bot.reply_to(message, message.chat.id)


@bot.message_handler(commands=['status'])
def get_order_status(message):
    if CoffeeHouse.get_or_none(CoffeeHouse.chat_id == message.chat.id):
        order = Order.get_or_none(Order.id == message.text.split()[1])
        if order is not None:
            bot.send_message(chat_id=message.chat.id, text=f'Статус заказа №{order.id}: {order.get_status_name()}')
        else:
            bot.send_message(chat_id=message.chat.id, text=f'Заказ с номером {message.text} не найден')


@bot.message_handler(commands=['bug_report', 'feed_back'])
def send_bug_report(message):
    msg = '<b>BUG REPORT</b>\n'
    if message.text.split()[0] == '/feed_back':
        msg = '<b>FEED BACK</b>\n'
    msg += message.text
    bot.send_message(chat_id=-487736638, text=msg, parse_mode='HTML')


@bot.message_handler(content_types=['contact'])
def contact_handler(message):
    phone_number = message.contact.phone_number
    if message.contact.user_id != message.from_user.id:
        bot.send_message(chat_id=message.chat.id,
                         text='Это НЕ ваш номер телефона.')
        return

    if customer := Customer.get_or_none(phone_number=phone_number[-10:]):
        customer.confirmed = True
        customer.chat_id = message.chat.id
        customer.save()

        bot.send_message(chat_id=message.chat.id,
                         text='Номер телефона подтвержден.',
                         reply_markup=types.ReplyKeyboardRemove(
                             selective=False))
    else:
        bot.send_message(chat_id=message.chat.id,
                         text='Пользователь с таким номером телефона не найден.')


@bot.callback_query_handler(func=lambda call: True)
def callback_processing(call: types.CallbackQuery):
    cb_status, order_number = map(int, call.data.split())
    order = Order.get_or_none(id=int(order_number))
    order.status = cb_status
    order.save()

    ans = 'Заказ принят' if cb_status == 1 else 'Заказ отклонен'
    bot.answer_callback_query(call.id, ans)
    ans = f"\n<b>{ans}</b>"
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text=call.message.text + ans, parse_mode='HTML',
                          reply_markup=None)
