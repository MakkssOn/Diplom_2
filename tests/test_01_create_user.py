import requests
import allure
from data.data_url import DataUrl
from data.expected_responses import expected_responses

@allure.story("1. Создание пользователя")
class TestCreateUser:
    endpoint = "/auth/register"

    @allure.title("Создание уникального пользователя")
    def test_create_unique_user(self, create_user_data):
        response = requests.post(DataUrl.BASE_URL + self.endpoint, json=create_user_data)

        assert response.status_code == 200
        assert response.json().get("success") is True
        assert "accessToken" in response.json()
        assert "refreshToken" in response.json()

    @allure.title("Создание пользователя, который уже зарегистрирован")
    def test_create_existing_user(self, persistent_user_data):
        response = requests.post(DataUrl.BASE_URL + self.endpoint, json=persistent_user_data)

        assert response.status_code == 403
        assert response.json() == expected_responses["create_user"]["existing_user_status"]

    @allure.title("Создание пользователя с пропуском обязательного поля")
    def test_create_user_missing_field(self):
        data = {
            "email": "new_user_missing_field@example.com",
            "password": "securePassword123"
            # Отсутствует поле "name"
        }
        response = requests.post(DataUrl.BASE_URL + self.endpoint, json=data)

        assert response.status_code == 403
        assert response.json() == expected_responses["create_user"]["missing_field_status"]