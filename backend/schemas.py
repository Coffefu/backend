from datetime import datetime, timedelta

from pydantic import BaseModel, validator, constr
from pytz import timezone


class Customer(BaseModel):
    name: constr(max_length=20)
    phone_number: constr(max_length=20)
    email: constr(max_length=100)


class Order(BaseModel):
    coffee_house: str  # TEST maybe int
    customer: Customer
    product: int
    time: datetime

    # REDO Order time_validator
    @validator('time')
    def time_validator(cls, future: datetime):
        future = timezone('Asia/Vladivostok').localize(future)

        now = datetime.now(tz=timezone('Asia/Vladivostok'))
        min_time = timedelta(minutes=5)
        max_time = timedelta(hours=5)

        assert now < future and min_time <= future - now <= max_time, \
            "Incorrect order time. The allowed time is from 5 minutes to 5 hours"

        return future