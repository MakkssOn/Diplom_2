import pytest
from data.data_url import DataUrl
from data.test_data import TestData
from api.user_api import UserAPI
from api.ingredients_api import IngredientsAPI
from api.orders_api import OrdersAPI

user_api = UserAPI()
ingredients_api = IngredientsAPI()
orders_api = OrdersAPI()

@pytest.fixture(scope="class")
def auth_token():
    user_data = TestData.unique_user()
    response = user_api.create_user(user_data)
    token = response.json().get("accessToken")
    
    yield token
    
    user_api.delete_user(token)

@pytest.fixture(scope="class")
def ingredients():
    response = ingredients_api.get_ingredients()
    return [item["_id"] for item in response.json().get("data", [])]

@pytest.fixture(scope="class")
def create_user_data():
    user_data = TestData.unique_user()
    response = user_api.create_user(user_data)
    token = response.json().get("accessToken")
    
    yield {"user_data": user_data, "token": token}
    
    user_api.delete_user(token)

@pytest.fixture(scope="class")
def persistent_user_data():
    return TestData.persistent_user()

@pytest.fixture(scope="class")
def create_order(auth_token, ingredients):
    order_data = {"ingredients": ingredients[:2]}
    response = orders_api.create_order(auth_token, order_data)
    order_id = response.json().get("order").get("number")
    
    yield response.json()
    
    orders_api.delete_order(auth_token, order_id)
