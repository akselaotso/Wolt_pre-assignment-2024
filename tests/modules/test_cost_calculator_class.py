from delivery_fee_calculator.modules.cost_calculator_class import CostCalculator
from datetime import datetime

def test_cost_calculator():
    delivery = CostCalculator(cart_value = 790, delivery_distance = 2235, number_of_items = 4, time = datetime(2024, 1, 21, 0, 0, 0))
    assert delivery.final_price() == 710

