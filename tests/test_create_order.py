import allure
import requests

from data import Urls, TextAnswer, Ingredients


class TestCreateOrder:
    @allure.title("Создание заказа с атворизацией и ингредиентами")
    def test_auth_create_order(self, create_user):

        respons_created, data = create_user
        del data["name"]
        requests.post(Urls.LOGIN_USER, data=data)
        ingredients = {"ingredients": [Ingredients.BUN, Ingredients.KOKLETA, Ingredients.SAUCE, Ingredients.BUN]}
        resp = requests.post(Urls.CREATE_ORDER, data=ingredients)

        assert resp.status_code == 200 and TextAnswer.TRUE in resp.text

    @allure.title("Создание заказа без авторизации и с ингридиентами")
    def test_no_auth_create_order(self):

        ingredients = {"ingredients": [Ingredients.BUN, Ingredients.KOKLETA, Ingredients.SAUCE, Ingredients.BUN]}
        resp = requests.post(Urls.CREATE_ORDER, data=ingredients)

        assert resp.status_code == 200 and TextAnswer.TRUE in resp.text

    @allure.title("Создание заказа с авторизацией и без ингридиентов")
    def test_auth_create_order_without_ingredients(self, create_user):

        respons_created, data = create_user
        del data["name"]
        requests.post(Urls.LOGIN_USER, data=data)
        ingredients = {"ingredients": ['']}
        resp = requests.post(Urls.CREATE_ORDER, data=ingredients)

        assert resp.status_code == 400 and TextAnswer.NOT_INGREDIENT in resp.text

    @allure.title("Создание заказ без авторизации и с неправильным хешем ингридиента")
    def test_no_auth_create_order_incorrect_hash(self):

        ingredients = {"ingredients": [Ingredients.ENIGMA, Ingredients.KOKLETA]}
        resp = requests.post(Urls.CREATE_ORDER, data=ingredients)

        assert resp.status_code == 500 and TextAnswer.ORDER_INCORRECT_INGREDIENTS in resp.text
