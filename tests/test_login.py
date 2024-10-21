import allure
import requests

from data import Urls, TextAnswer
from methods import Methods


class TestLogin:
    @allure.title("Логин под существующим пользователем")
    def test_login_existing_user(self, create_user):

        respons_created, data = create_user
        del data["name"]
        resp = requests.post(Urls.LOGIN_USER, data=data)

        assert resp.status_code == 200 and TextAnswer.TRUE in resp.text

    @allure.title("Логин с неверным логином и паролем")
    def test_login_with_incorrect_data(self):

        methods = Methods()
        user_data = methods.generate_user_data()
        del user_data["name"]
        resp = requests.post(Urls.LOGIN_USER, data=user_data)

        assert resp.status_code == 401 and TextAnswer.INCORRECT_DATA

    @allure.title("Логин с неверным паролем")
    def test_login_with_incorrect_pass(self, create_user):

        respons_created, data = create_user

        del data["name"]
        data['password'] = ''
        resp = requests.post(Urls.LOGIN_USER, data=data)

        assert resp.status_code == 401 and TextAnswer.INCORRECT_DATA

    @allure.title("Логин с неверным логином ")
    def test_login_with_incorrect_login(self, create_user):

        respons_created, data = create_user
        del data["name"]
        data['email'] = ''
        resp = requests.post(Urls.LOGIN_USER, data=data)

        assert resp.status_code == 401 and TextAnswer.INCORRECT_DATA
