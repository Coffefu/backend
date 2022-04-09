from datetime import datetime

from peewee import \
    ForeignKeyField, CharField, DateTimeField, IntegerField, TimeField, BooleanField, Check

from db import BaseModel


class Customer(BaseModel):
    name = CharField(max_length=20)
    phone_number = CharField(max_length=10)
    confirmed = BooleanField(default=False)
    chat_id = IntegerField(null=True)

    def __str__(self):
        return f'name: {self.name}, phone_number: {self.phone_number}, email: {self.email}'

    class Meta:
        table_name = 'customers'


class Product(BaseModel):
    ProductTypes = (
        (0, 'Кофе'),
        (1, 'Не кофе')
    )
    type = IntegerField(choices=ProductTypes, default=0)
    name = CharField(max_length=20)
    description = CharField(max_length=200, null=True)
    img = CharField(max_length=200, null=True)

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
    OrderStatus = (
        (0, 'В ожидании'),
        (1, 'Принят'),
        (2, 'Отклонен'),
        (3, 'Выполнен'),
        (4, 'Не выполнен')
    )
    coffee_house = ForeignKeyField(CoffeeHouse, backref='coffee_house')
    customer = ForeignKeyField(Customer, backref='customer')
    time = DateTimeField()
    status = IntegerField(default=0, choices=OrderStatus)

    class Meta:
        table_name = 'orders'

    def get_status_name(self):
        return dict(self.OrderStatus)[self.status]


class OrderedProduct(BaseModel):
    order = ForeignKeyField(Order)
    product = ForeignKeyField(ProductVarious)


class Worktime(BaseModel):
    DaysOfWeek = (
        (0, 'Понедельник'),
        (1, 'Вторник'),
        (2, 'Среда'),
        (3, 'Четверг'),
        (4, 'Пятница'),
        (5, 'Суббота'),
        (6, 'Воскресенье'),
    )
    day_of_week = IntegerField(choices=DaysOfWeek)
    open_time = TimeField(formats='%H:%M:%S')
    close_time = TimeField(formats='%H:%M:%S')

    def get_day_of_week_name(self):
        return dict(self.DaysOfWeek)[self.day_of_week]


class TimeTable(BaseModel):
    worktime = ForeignKeyField(Worktime)
    coffee_house = ForeignKeyField(CoffeeHouse, backref='coffee_house')


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
