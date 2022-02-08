from fastapi import FastAPI, HTTPException
from starlette.responses import FileResponse
import telebot
import logging

from app.models import *
from backend import schemas
from backend.settings import API_TOKEN, SERVER_PORT, WEBHOOK_SSL_CERT, DOMAIN
from bot import bot
from bot.bot_funcs import send_order

app = FastAPI(redoc_url=None, docs_url=None)


@app.on_event("startup")
async def on_startup():
    bot.remove_webhook()
    bot.set_webhook(url=f"https://{DOMAIN}:{SERVER_PORT}" + f'/{API_TOKEN}/',
                    certificate=open(WEBHOOK_SSL_CERT, 'r'))


@app.on_event("shutdown")
async def on_shutdown():
    await bot.session.close()


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
    customer: Customer = Customer.get_or_create(**dict(order.customer))[0]
    coffee_house: CoffeeHouse = CoffeeHouse.get_or_none(CoffeeHouse.name == order.coffee_house)
    product: Product = Product.get_or_none(Product.id == order.product)

    if coffee_house is None:
        return HTTPException(400, 'Incorrect coffee house')
    if product is None:
        return HTTPException(400, 'Incorrect product')

    order = Order.create(coffee_house=coffee_house, customer=customer, product=product, time=order.time)
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
