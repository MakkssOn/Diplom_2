import requests
import pytest
import uuid
from typing import Dict, Any, List
from data.data_url import DataUrl


class APIError(Exception):
    """Кастомное исключение для ошибок API."""
    pass


def validate_response(response: requests.Response, expected_status: int = 200) -> Dict[str, Any]:
    """Валидация ответа API."""
    if response.status_code != expected_status:
        raise APIError(f"Unexpected status code: {response.status_code}. Response: {response.text}")
    return response.json()


@pytest.fixture(scope="class")
def random_email() -> str:
    """Генерация уникального email."""
    return f"{uuid.uuid4()}@example.com"


@pytest.fixture(scope="class")
def base_user_data(random_email: str) -> Dict[str, Any]:
    """Базовые данные пользователя."""
    return {
        "email": random_email,
        "password": "securePassword123!",
        "name": "TestUser"
    }


@pytest.fixture(scope="class")
def auth_token(base_user_data: Dict[str, Any], request: pytest.FixtureRequest) -> str:
    """Фикстура для получения auth токена с автоматическим удалением пользователя после тестов."""
    # Регистрация пользователя
    reg_response = requests.post(DataUrl.BASE_URL + "/auth/register", json=base_user_data)
    auth_data = validate_response(reg_response, 200)
    token = auth_data.get("accessToken")
    
    if not token:
        raise APIError("No access token in registration response")

    # Функция для удаления пользователя после тестов
    def delete_user():
        headers = {"Authorization": token}
        del_response = requests.delete(DataUrl.BASE_URL + "/auth/user", headers=headers)
        try:
            validate_response(del_response, 202)
        except APIError as e:
            pytest.fail(f"Failed to delete user: {str(e)}")

    request.addfinalizer(delete_user)
    return token


@pytest.fixture(scope="class")
def ingredients() -> List[str]:
    """Фикстура для получения списка доступных ингредиентов."""
    response = requests.get(DataUrl.BASE_URL + "/ingredients")
    data = validate_response(response, 200)
    return [item["_id"] for item in data.get("data", []) if "_id" in item]


@pytest.fixture(scope="class")
def create_order(auth_token: str, ingredients: List[str], request: pytest.FixtureRequest) -> Dict[str, Any]:
    """Фикстура для создания заказа с автоматическим удалением после тестов."""
    if len(ingredients) < 2:
        pytest.skip("Not enough ingredients to create order")
    
    headers = {"Authorization": auth_token}
    order_data = {"ingredients": ingredients[:2]}  # Используем первые два ингредиента
    
    response = requests.post(DataUrl.BASE_URL + "/orders", headers=headers, json=order_data)
    order_data = validate_response(response, 200)
    
    order_number = order_data.get("order", {}).get("number")
    if not order_number:
        raise APIError("No order number in response")

    # Функция для удаления заказа (если API поддерживает)
    def cleanup():
        try:
            requests.delete(DataUrl.BASE_URL + f"/orders/{order_number}", headers=headers)
        except Exception as e:
            print(f"Order cleanup warning: {str(e)}")

    request.addfinalizer(cleanup)
    return order_data


@pytest.fixture(scope="session")
def persistent_user() -> Dict[str, Any]:
    """Фикстура для создания постоянного тестового пользователя (не удаляется)."""
    user_data = {
        "email": f"persistent_{uuid.uuid4()}@example.com",
        "password": "securePassword123!",
        "name": "PersistentUser"
    }
    
    try:
        response = requests.post(DataUrl.BASE_URL + "/auth/register", json=user_data)
        if response.status_code == 403:
            # Пользователь уже существует - попробуем войти
            login_response = requests.post(DataUrl.BASE_URL + "/auth/login", json={
                "email": user_data["email"],
                "password": user_data["password"]
            })
            validate_response(login_response, 200)
        else:
            validate_response(response, 200)
    except Exception as e:
        pytest.skip(f"Failed to create persistent user: {str(e)}")
    
    return user_data