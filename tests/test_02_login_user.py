import requests
import allure
from data.data_url import DataUrl
from data.expected_responses import expected_responses

@allure.story("2. Логин пользователя")
class TestLoginUser:
    endpoint_login = "/auth/login"

    @allure.title("Логин под существующим пользователем")
    def test_login_existing_user(self, persistent_user_data):
        response = requests.post(DataUrl.BASE_URL + self.endpoint_login, json=persistent_user_data)

        assert response.status_code == 200
        assert response.json().get("success") is True
        assert "accessToken" in response.json()

    @allure.title("Логин с неверным логином и паролем")
    def test_login_incorrect_credentials(self):
        incorrect_data = {
            "email": "nonexistent_user@example.com",
            "password": "wrongPassword"
        }
        response = requests.post(DataUrl.BASE_URL + self.endpoint_login, json=incorrect_data)

        assert response.status_code == 401
        assert response.json() == expected_responses["login_user"]["incorrect_credentials_status"]