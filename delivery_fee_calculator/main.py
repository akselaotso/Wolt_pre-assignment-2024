from .modules.cost_calculator_class import CostCalculator
from fastapi import FastAPI
from pydantic import BaseModel, Field
from datetime import datetime

# testaa - numerot, random str time tilalla, testaa 0:t
class DeliveryInformationRequest(BaseModel):
    cart_value: int = Field(ge = 0)
    delivery_distance: int  = Field(ge = 0)
    number_of_items: int  = Field(ge = 0)
    time: datetime

app = FastAPI()

@app.post("/")
def read_item(delivery_information: DeliveryInformationRequest):
    delivery = CostCalculator(
        cart_value = delivery_information.cart_value, 
        delivery_distance = delivery_information.delivery_distance, 
        number_of_items = delivery_information.number_of_items, 
        time = delivery_information.time
    )

    fee: int = delivery.final_price()

    return {'delivery_fee': fee}

