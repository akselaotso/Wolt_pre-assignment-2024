#Wolt 2024 Software Engineering Internship Preassignment, Backend assignment with Python

###Table of contents:
[Introduction](#introduction)  
[Running app](#running)
[Specific calculation rules](#calculation)

<a name="introduction">
##Introduction

Assignment details directly from [Wolt's instructions](https://github.com/woltapp/engineering-internship-2024#)

This is my README.md for my Wolt internship preassignment, I completed the backend assignment with Python. The assignment entailed a HTTP API with a single POST endpoint which, when presented with cart value, delivery distance, number of items and time, would calculate the delivery fee. 

A proper POST request would be in the following format: 
```json
{"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "2024-01-15T13:00:00Z"}
```

A proper response:
```json
{"delivery_fee": 710}
```

The app itself is located in delivery_fee_calculator/ with the API being located in delivery_fee_calculator/main.py and the calculator in delivery_fee_calculator/modules/cost_calculator.class.py. 

This projects' testing gravitated toward API itself in tests/test_main.py, with a single checkup test in tests/modules/test_cost_calculator_class.py. 


<a name="running">
##Running app

The app uses poetry as a package manager, FastAPI for the API and pytest for testing. If poetry is not installed, it has to be installed before proceeding. 

Install app:
```
poetry install
```

Run tests:
```
poetry run pytest
```

Start server:
```
poetry run uvicorn delivery_fee_calculator.main:app --reload
```

Example curl command:
```
curl -X POST http://127.0.0.1:8000 -H 'Content-Type: application/json' -d '{"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "2024-01-15T13:00:00Z"}'
```


<a name="calculation">
##Specific calculation rules

Rules for calculating a delivery fee, directly from [Wolt's instructions](https://github.com/woltapp/engineering-internship-2024#)
* If the cart value is less than 10€, a small order surcharge is added to the delivery price. The surcharge is the difference between the cart value and 10€. For example if the cart value is 8.90€, the surcharge will be 1.10€.
* A delivery fee for the first 1000 meters (=1km) is 2€. If the delivery distance is longer than that, 1€ is added for every additional 500 meters that the courier needs to travel before reaching the destination. Even if the distance would be shorter than 500 meters, the minimum fee is always 1€.
    * Example 1: If the delivery distance is 1499 meters, the delivery fee is: 2€ base fee + 1€ for the additional 500 m => 3€
    * Example 2: If the delivery distance is 1500 meters, the delivery fee is: 2€ base fee + 1€ for the additional 500 m => 3€
    * Example 3: If the delivery distance is 1501 meters, the delivery fee is: 2€ base fee + 1€ for the first 500 m + 1€ for the second 500 m => 4€
* If the number of items is five or more, an additional 50 cent surcharge is added for each item above and including the fifth item. An extra "bulk" fee applies for more than 12 items of 1,20€
    * Example 1: If the number of items is 4, no extra surcharge
    * Example 2: If the number of items is 5, 50 cents surcharge is added
    * Example 3: If the number of items is 10, 3€ surcharge (6 x 50 cents) is added
    * Example 4: If the number of items is 13, 5,70€ surcharge is added ((9 * 50 cents) + 1,20€)
    * Example 5: If the number of items is 14, 6,20€ surcharge is added ((10 * 50 cents) + 1,20€)
* The delivery fee can __never__ be more than 15€, including possible surcharges.
* The delivery is free (0€) when the cart value is equal or more than 200€. 
* During the Friday rush, 3 - 7 PM, the delivery fee (the total fee including possible surcharges) will be multiplied by 1.2x. However, the fee still cannot be more than the max (15€). Considering timezone, for simplicity, **use UTC as a timezone in backend solutions** (so Friday rush is 3 - 7 PM UTC). **In frontend solutions, use the timezone of the browser** (so Friday rush is 3 - 7 PM in the timezone of the browser).

