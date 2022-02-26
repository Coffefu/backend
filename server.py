from fastapi import FastAPI, HTTPException
from starlette.responses import FileResponse
import telebot
import logging

from app.models import *
from backend import schemas
from backend.settings import API_TOKEN, WEBHOOK_SSL_CERT, DOMAIN, SERVER_PORT
from bot import bot
from bot.bot_funcs import send_order
from bot.email_sender import send_email

app = FastAPI(redoc_url=None, docs_url=None)


@app.on_event("startup")
async def on_startup():
    pass
    # bot.remove_webhook()
    # bot.set_webhook(url=f"https://{DOMAIN}:{SERVER_PORT}" + f'/{API_TOKEN}/',
    #                 certificate=open(WEBHOOK_SSL_CERT, 'r'))


@app.get('/products')
async def get_products():
    return [p.data(hide=['description']) for p in Product.select()]


# TEST return svg or ico depending on the user's browser
@app.get('/favicon.svg')
async def get_favicon_svg():
    return FileResponse('assets/beans.svg')


@app.get('/favicon.ico')
async def get_favicon_svg():
    return FileResponse('assets/beans.ico')


@app.post('/make_order')
async def make_order(order: schemas.Order):
    print(order)

    # coffee_house: CoffeeHouse = CoffeeHouse.get_or_none(CoffeeHouse.name == order.coffee_house)
    # if coffee_house is None:
    #     return HTTPException(400, 'Incorrect coffee house')
    #
    # customer: Customer = Customer.get_or_create(**dict(order.customer))[0]
    # for prod in order.products:
    #     product: Product = Product.get_or_none(Product.id == prod)
    #     if product is None:
    #         return HTTPException(400, 'Incorrect product')





    order = Order.create(coffee_house=coffee_house, customer=customer, time=order.time)
    send_order({'order_number': order.id,
                'product_name': product.name,
                'time': order.time,
                'customer_name': customer.name,
                'phone_number': customer.phone_number,
                'email': customer.email,
                'coffee_house_chat_id': coffee_house.chat_id, })
    return 'Success'


@app.post(f'/{API_TOKEN}/')
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

    customer_email = Order.get_or_none(id=int(order_number)).customer.email
    status = cb_ans == 'yes'
    send_email(customer_email, int(order_number), status)
    # вызовем функцию САНИ
    # вызовем функцию отправки EMAIL

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=call.message.text + ans, reply_markup=None)
