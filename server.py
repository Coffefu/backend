from fastapi import FastAPI
from fastapi import HTTPException

from backend.settings import BOT_MODULE_PATH

from app.models import *
from backend import schemas

from importlib import import_module

bot = import_module(BOT_MODULE_PATH)
app = FastAPI(redoc_url=None, docs_url=None)


@app.get('/products')
async def get_products():
    return [p.data(hide=['description']) for p in Product.select()]


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

    bot.send_order({'order_number': order.id,
                    'product_name': product.name,
                    'time': order.time,
                    'customer_name': customer.name,
                    'phone_number': customer.phone_number,
                    'email': customer.email,
                    'coffee_house_chat_id': coffee_house.chat_id, })

    return 'Success'
