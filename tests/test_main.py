from fastapi.testclient import TestClient
from delivery_fee_calculator.main import app
import pytest
import json

client = TestClient(app)

def test_proper_request():
    response = client.post(
        "/",
        json = {"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "2024-01-15T13:00:00Z"},
    )
    assert response.status_code == 200
    assert response.json() == {"delivery_fee": 710}


def test_no_json_request():
    response = client.post(
        "/"
    )
    assert response.status_code == 422
    assert response.json() == {'detail': [{
        'input': None, 
        'loc': ['body'], 
        'msg': 'Field required', 
        'type': 'missing', 
        'url': 'https://errors.pydantic.dev/2.5/v/missing'
        }]
    }


def test_missing_information_request():
    response = client.post(
        "/",
        json = {"cart_value": 790, "delivery_distance": 2235, "time": "2024-01-15T13:00:00Z"},
    )
    assert response.status_code == 422
    assert response.json() == { 'detail': [{
        'input': {
            'cart_value': 790,
            'delivery_distance': 2235,
            'time': '2024-01-15T13:00:00Z'},
            'loc': ['body','number_of_items'],
            'msg': 'Field required',
            'type': 'missing',
            'url': 'https://errors.pydantic.dev/2.5/v/missing'}]
            }


input_value_type_test_ids = [
    "negative cart_value", 
    "negative delivery_distance", 
    "negative number_of_items", 
    "invalid time string", 
    "invalid string as cart_value",
    "invalid string as delivery_distance",
    "invalid string as number_of_items",
    "too large timestamp as time",
    "valid integer in string format for cart_value, delivery_distance and number_of_items",
    "multiple incorrect inputs"
]
input_value_type_test_values = [
    (-790, 2235, 4, "2024-01-15T13:00:00Z", 422, {"detail":[{
        "type":"greater_than_equal",
        "loc":["body","cart_value"],
        "msg":"Input should be greater than or equal to 0",
        "input":-790,
        "ctx":{"ge":0},
        "url":"https://errors.pydantic.dev/2.5/v/greater_than_equal"
        }]}
    ), 
    (790, -2235, 4, "2024-01-15T13:00:00Z", 422, {"detail":[{
        "type":"greater_than_equal",
        "loc":["body","delivery_distance"],
        "msg":"Input should be greater than or equal to 0",
        "input":-2235,
        "ctx":{"ge":0},
        "url":"https://errors.pydantic.dev/2.5/v/greater_than_equal"
        }]}
    ), 
    (790, 2235, -4, "2024-01-15T13:00:00Z", 422, {"detail":[{
        "type":"greater_than_equal",
        "loc":["body","number_of_items"],
        "msg":"Input should be greater than or equal to 0",
        "input":-4,
        "ctx":{"ge":0},
        "url":"https://errors.pydantic.dev/2.5/v/greater_than_equal"
        }]}
    ), 
    (790, 2235, 4, "asdafasdfas", 422, {"detail":[{
        "type":"datetime_parsing",
        "loc":["body","time"],
        "msg":"Input should be a valid datetime, invalid character in year",
        "input":"asdafasdfas",
        "ctx":{"error":"invalid character in year"},
        "url":"https://errors.pydantic.dev/2.5/v/datetime_parsing"}]}
    ), 
    ("aaaa", 2235, 4, "2024-01-15T13:00:00Z", 422, {"detail":[{
        "type":"int_parsing",
        "loc":["body","cart_value"],
        "msg":"Input should be a valid integer, unable to parse string as an integer",
        "input":"aaaa",
        "url":"https://errors.pydantic.dev/2.5/v/int_parsing"}]}
    ), 
    (790, "aaaa", 4, "2024-01-15T13:00:00Z", 422, {"detail":[{
        "type":"int_parsing",
        "loc":["body","delivery_distance"],
        "msg":"Input should be a valid integer, unable to parse string as an integer",
        "input":"aaaa",
        "url":"https://errors.pydantic.dev/2.5/v/int_parsing"}]}
    ), 
    (790, 2235, "aaaa", "2024-01-15T13:00:00Z", 422, {"detail":[{
        "type":"int_parsing",
        "loc":["body","number_of_items"],
        "msg":"Input should be a valid integer, unable to parse string as an integer",
        "input":"aaaa",
        "url":"https://errors.pydantic.dev/2.5/v/int_parsing"}]}
    ), 
    (790, 2235, 4, 99999999999999999, 422, {"detail":[{
        "type":"datetime_parsing",
        "loc":["body","time"],
        "msg":"Input should be a valid datetime, dates after 9999 are not supported as unix timestamps",
        "input":99999999999999999,
        "ctx":{"error":"dates after 9999 are not supported as unix timestamps"},
        "url":"https://errors.pydantic.dev/2.5/v/datetime_parsing"}]}
    ), 
    ("790", "2235", "4", "2024-01-15T13:00:00Z", 200, {"delivery_fee": 710}),
    (790, 2235, -4, "asdasdasd", 422, {"detail":[{
            "type":"greater_than_equal",
            "loc":["body","number_of_items"],
            "msg":"Input should be greater than or equal to 0",
            "input":-4,"ctx":{"ge":0},
            "url":"https://errors.pydantic.dev/2.5/v/greater_than_equal"
        },{
            "type":"datetime_parsing",
            "loc":["body","time"],
            "msg":"Input should be a valid datetime, input is too short",
            "input":"asdasdasd",
            "ctx":{"error":"input is too short"},
            "url":"https://errors.pydantic.dev/2.5/v/datetime_parsing"}]}
    )
]
@pytest.mark.parametrize("cart_value, delivery_distance, number_of_items, time, status_code, result", input_value_type_test_values, ids=input_value_type_test_ids)
def test_wrong_input_request(cart_value, delivery_distance, number_of_items, time, status_code, result):
    response = client.post(
        "/",
        json = {"cart_value": cart_value, "delivery_distance": delivery_distance, "number_of_items": number_of_items, "time": time},
    )
    assert response.status_code == status_code 
    assert response.json() == result


cart_value_test_values = [(790, 410), (0, 1200), (1000, 200), (999, 201), (19999, 200), (20000, 0), (20001, 0)]
@pytest.mark.parametrize("value, result", cart_value_test_values)
def test_cart_value_request(value, result):
    response = client.post(
        "/",
        json = {"cart_value": value, "delivery_distance": 0, "number_of_items": 0, "time": "2024-01-15T13:00:00Z"},
    )
    assert response.status_code == 200
    assert response.json() == {"delivery_fee": result}


delivery_distance_test_values = [(0, 200), (499, 200), (999, 200), (1000, 200), (1001, 300), (1499, 300), (1500, 300), (1501, 400), (100000, 1500)]
@pytest.mark.parametrize("value, result", delivery_distance_test_values)
def test_delivery_distance_request(value, result):
    response = client.post(
        "/",
        json = {"cart_value": 1000, "delivery_distance": value, "number_of_items": 0, "time": "2024-01-15T13:00:00Z"},
    )
    assert response.status_code == 200
    assert response.json() == {"delivery_fee": result}


number_of_items_test_values = [(0, 200), (4, 200), (5, 250), (10, 500), (12, 600), (13, 770), (14, 820), (99, 1500)]
@pytest.mark.parametrize("value, result", number_of_items_test_values)
def test_number_of_items_request(value, result):
    response = client.post(
        "/",
        json = {"cart_value": 1000, "delivery_distance": 0, "number_of_items": value, "time": "2024-01-15T13:00:00Z"},
    )
    assert response.status_code == 200
    assert response.json() == {"delivery_fee": result}


time_test_values = [
    ("2024-01-19T14:59:00Z", 200), 
    ("2024-01-19T15:00:00Z", 240), 
    ("2024-01-19T17:30:00Z", 240), 
    ("2024-01-19T19:00:00Z", 240), 
    ("2024-01-19T19:01:00Z", 200), 
    ("2024-01-18T15:00:00Z", 200), 
    ("2024-01-18T17:30:00Z", 200), 
    ("2024-01-18T19:00:00Z", 200)
]
@pytest.mark.parametrize("value, result", time_test_values)
def test_time_request(value, result):
    response = client.post(
        "/",
        json = {"cart_value": 1000, "delivery_distance": 0, "number_of_items": 0, "time": value},
    )
    assert response.status_code == 200
    assert response.json() == {"delivery_fee": result}

