from math import ceil 
from datetime import time


class CostCalculator:
    fee_per_500m: int = 100
    charge_per_item: int = 50
    bulk_charge: int = 120
    bulk_charge_limit: int = 12
    max_price: int = 1500
    rush_hour_multiplier: float = 1.2
    small_order_surcharge_limit: int = 1000
    minimum_delivery_fee: int = 200
    minimum_distance_limit: int = 1000
    rush_hour_weekday: int = 4
    rush_hour_start: time = time(15, 0)
    rush_hour_end: time = time(19, 0)

    def __init__(self, cart_value: int, delivery_distance: int, number_of_items: int, time: str) -> None:
        self.cart_value = cart_value
        self.delivery_distance = delivery_distance
        self.number_of_items = number_of_items
        self.time = time

    def __surcharge(self) -> int:
        if self.cart_value <= self.small_order_surcharge_limit:
            return self.small_order_surcharge_limit - self.cart_value
        return 0

    def __delivery_distance_charge(self) -> int:
        if self.delivery_distance < self.minimum_distance_limit:
            return self.minimum_delivery_fee

        delivery_distance_charge: int = ceil(self.delivery_distance / 500.0) * self.fee_per_500m

        return delivery_distance_charge

    def __item_charge(self) -> int:
        if self.number_of_items < 5:
            return 0

        number_of_items_with_charge: int = self.number_of_items - 4

        item_charge: int = number_of_items_with_charge * self.charge_per_item

        if self.number_of_items > self.bulk_charge_limit:
            return item_charge + self.bulk_charge

        return item_charge

    def __is_rush_hour(self) -> bool:
        if self.time.weekday() == self.rush_hour_weekday and self.rush_hour_start <= self.time.time() <= self.rush_hour_end:
            return True

        return False

    def final_price(self) -> int:
        if self.cart_value >= 20000:
            return 0

        delivery_fee: int = self.__item_charge() + self.__delivery_distance_charge() + self.__surcharge()

        if self.__is_rush_hour():
            delivery_fee = int(delivery_fee * self.rush_hour_multiplier)

        if delivery_fee >= self.max_price:
            return self.max_price

        return delivery_fee

