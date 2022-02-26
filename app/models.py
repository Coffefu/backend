from datetime import datetime

from peewee import \
    ForeignKeyField, CharField, DateTimeField, IntegerField, TimeField, BooleanField, Check

from db import BaseModel


class Customer(BaseModel):
    name = CharField(max_length=20)
    phone_number = CharField(max_length=20)
    email = CharField(max_length=100)  # Maybe less characters

    def __str__(self):
        return f'name: {self.name}, phone_number: {self.phone_number}, email: {self.email}'

    class Meta:
        table_name = 'customers'


class Product(BaseModel):
    name = CharField(max_length=20)
    description = CharField(max_length=200, null=True)
    img = CharField(max_length=200)

    def __str__(self):
        return f'name: {self.name}'

    class Meta:
        table_name = 'products'


class ProductVarious(BaseModel):
    product = ForeignKeyField(Product)
    size = IntegerField(constraints=[Check('size >= 0')])
    price = IntegerField(constraints=[Check('size >= 0')])


class CoffeeHouse(BaseModel):
    name = CharField(max_length=20)
    placement = CharField(max_length=20)
    chat_id = IntegerField()
    is_open = BooleanField()

    def __str__(self):
        return f'name: {self.name}, placement: {self.placement}'

    class Meta:
        table_name = 'coffeehouses'


class Order(BaseModel):
    coffee_house = ForeignKeyField(CoffeeHouse, backref='coffee_house')
    customer = ForeignKeyField(Customer, backref='customer')
    time = DateTimeField()
    status = IntegerField(default=0)

    class Meta:
        table_name = 'orders'


class OrderedProduct(BaseModel):
    order = ForeignKeyField(Order)
    product = ForeignKeyField(Product)


DaysOfWeek = (
    ('MON', 'Понедельник'),
    ('TUE', 'Вторник'),
    ('WED', 'Среда'),
    ('THU', 'Четверг'),
    ('FRI', 'Пятница'),
    ('SAT', 'Суббота'),
    ('SUN', 'Воскресенье'),
)


class Worktime(BaseModel):
    day_of_week = CharField(max_length=3, choices=DaysOfWeek)
    open_time = TimeField()
    close_time = TimeField()


class TimeTable(BaseModel):
    worktime = ForeignKeyField(Worktime)
    coffee_house = ForeignKeyField(CoffeeHouse)


class Topping(BaseModel):
    name = CharField(max_length=100)
    price = IntegerField(constraints=[Check('price >= 0')])


class ToppingToProduct(BaseModel):
    ordered_product = ForeignKeyField(OrderedProduct)
    topping = ForeignKeyField(Topping)


if __name__ == '__main__':
    import db

    db.db.create_tables([Customer, Product, CoffeeHouse, Order, Worktime, TimeTable, ProductVarious,
                         OrderedProduct, ToppingToProduct, Topping])

__all__ = ['Customer', 'Product', 'CoffeeHouse', 'Order', 'Worktime', 'TimeTable', 'ProductVarious',
           'OrderedProduct', 'ToppingToProduct', 'Topping']
