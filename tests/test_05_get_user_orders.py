import requests
import allure
from data.data_url import DataUrl
from data.expected_responses import expected_responses

@allure.story("5. Получение заказов конкретного пользователя")
class TestGetUserOrders:
    endpoint_get_orders = "/orders"

    @allure.title("Получение заказов с авторизированным пользователем")
    def test_get_orders_with_auth(self, auth_token, create_order):
        headers = {"Authorization": auth_token}
        response = requests.get(DataUrl.BASE_URL + self.endpoint_get_orders, headers=headers)

        assert response.status_code == 200
        assert response.json().get("success") is True
        assert len(response.json().get("orders", [])) > 0

    @allure.title("Получение заказов с не авторизированным пользователем")
    def test_get_orders_without_auth(self):
        response = requests.get(DataUrl.BASE_URL + self.endpoint_get_orders)

        assert response.status_code == 401
        assert response.json() == expected_responses["login_user"]["unauthorized_status"]