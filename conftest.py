import requests
import pytest
import uuid
from data.data_url import DataUrl


@pytest.fixture(scope="class")
def auth_token(create_user_data):
    return create_user_data["token"]

@pytest.fixture(scope="class")
def ingredients():
    response = requests.get(DataUrl.BASE_URL + "/ingredients")
    ingredients = [item["_id"] for item in response.json().get("data", [])]
    return ingredients

@pytest.fixture(scope="class")
def create_user_data(request):
    unique_email = f"{uuid.uuid4()}@example.com"
    user_data = {
        "email": unique_email,
        "password": "securePassword123",
        "name": "UniqueUser"
    }
    response = requests.post(DataUrl.BASE_URL + "/auth/register", json=user_data)
    token = response.json().get("accessToken")

    def delete_user():
        headers = {"Authorization": token}
        requests.delete(DataUrl.BASE_URL + "/auth/user", headers=headers)

    request.addfinalizer(delete_user)
    return {"user_data": user_data, "token": token}

def unique_user_data(create_user):
    return create_user["user_data"]

@pytest.fixture(scope="class")
def create_order(auth_token, ingredients, request):
    headers = {"Authorization": auth_token}
    order_data = {"ingredients": ingredients[:2]}
    response = requests.post(DataUrl.BASE_URL + "/orders", headers=headers, json=order_data)
    assert response.status_code == 200, "Order creation failed in fixture"
    order_id = response.json().get("order").get("number")

    def delete_order():
        requests.delete(DataUrl.BASE_URL + f"/orders/{order_id}", headers=headers)

    request.addfinalizer(delete_order)
    return response.json()

@pytest.fixture(scope="class")
def persistent_user_data():
    """Фикстура для создания и возврата данных пользователя, который не удаляется после тестов."""
    email = "persistent_user@example.com"
    user_data = {
        "email": email,
        "password": "securePassword123",
        "name": "PersistentUser"
    }
    # Регистрация пользователя, если он еще не существует
    response = requests.post(DataUrl.BASE_URL + "/auth/register", json=user_data)
    if response.status_code not in [200, 403]:
        response.raise_for_status()
    return user_data