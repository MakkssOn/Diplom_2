import requests
import allure
from data.data_url import DataUrl
from data.expected_responses import expected_responses

@allure.story("4. Создание заказа")
class TestCreateOrder:
    endpoint_create_order = "/orders"
    endpoint_ingredients = "/ingredients"

    @allure.title("Создание заказа с авторизацией")
    def test_create_order_with_auth(self, auth_token, ingredients):
        headers = {"Authorization": auth_token}
        order_data = {"ingredients": ingredients[:2]}
        response = requests.post(DataUrl.BASE_URL + self.endpoint_create_order, headers=headers, json=order_data)

        assert response.status_code == 200
        assert response.json().get("success") is True

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(self, ingredients):
        order_data = {"ingredients": ingredients[:2]}
        response = requests.post(DataUrl.BASE_URL + self.endpoint_create_order, json=order_data)

        assert response.status_code == 401
        assert response.json() == expected_responses["login_user"]["unauthorized_status"]

    @allure.title("Создание заказа с ингредиентами")
    def test_create_order_with_ingredients(self, auth_token, ingredients):
        headers = {"Authorization": auth_token}
        order_data = {"ingredients": ingredients[:2]}
        response = requests.post(DataUrl.BASE_URL + self.endpoint_create_order, headers=headers, json=order_data)

        assert response.status_code == 200
        assert response.json().get("success") is True
        assert "order" in response.json()

    @allure.title("Создание заказа с пустым списком ингредиентов")
    def test_create_order_with_ingredients_with_auth(self, auth_token, ingredients):
        headers = {"Authorization": auth_token}
        order_data = {"ingredients": ingredients[:2]}
        response = requests.post(DataUrl.BASE_URL + self.endpoint_create_order, headers=headers, json=order_data)

        assert response.status_code == 200
        assert response.json().get("success") is True
        assert "order" in response.json()

    @allure.title("Создание заказа с пустым списком ингредиентов без авторизации")
    def test_create_order_with_empty_ingredients_without_auth(self):
        order_data = {"ingredients": []}
        response = requests.post(DataUrl.BASE_URL + self.endpoint_create_order, json=order_data)

        assert response.status_code == 401
        assert response.json() == expected_responses["login_user"]["unauthorized_status"]

    @allure.title("Создание заказа с пустым списком ингредиентов")
    def test_create_order_no_ingredients(self, auth_token):
        headers = {"Authorization": auth_token}
        order_data = {"ingredients": []}
        response = requests.post(DataUrl.BASE_URL + self.endpoint_create_order, headers=headers, json=order_data)

        assert response.status_code == 400
        assert response.json() == expected_responses["create_order"]["no_ingredients_status"]

    @allure.title("Создание заказа с неверным хешем ингредиента")
    def test_create_order_invalid_ingredient_hash(self, auth_token):
        headers = {"Authorization": auth_token}
        order_data = {"ingredients": ["invalid_hash"]}
        response = requests.post(DataUrl.BASE_URL + self.endpoint_create_order, headers=headers, json=order_data)

        assert response.status_code == 500
        assert response.json() == expected_responses["create_order"]["invalid_ingredient_hash_status"]