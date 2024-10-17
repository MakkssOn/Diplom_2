import allure
import requests

from data import Urls, TextAnswer


class TestChangingDataUsers:
    @allure.title("Изменение эмейла авторизованным пользаком")
    def test_auth_replacing_email_user(self, create_user):

        respons_created, data = create_user
        token = respons_created.json()['accessToken']
        headers = {"Content-type": "application/json", "Authorization": f'{token}'}
        new_email_value = 'x' + respons_created.json()["user"]['email']
        new_email = {"email": new_email_value}
        replace = requests.patch(Urls.REPLACE_DATA, json=new_email, headers=headers)

        assert replace.status_code == 200 and replace.json()['user']['email'] == new_email['email']

    @allure.title("Изменение пароля авторизованным пользаком")
    def test_auth_replacing_password_user(self, create_user):

        respons_created, data = create_user
        token = respons_created.json()['accessToken']
        headers = {"Content-type": "application/json", "Authorization": f'{token}'}
        new_password_value = 'x' + data["password"]
        new_password = {"password": new_password_value}
        replace = requests.patch(Urls.REPLACE_DATA, json=new_password, headers=headers)

        assert replace.status_code == 200 and TextAnswer.TRUE in replace.text

    @allure.title("Изменение имени авторизованным пользаком")
    def test_auth_replacing_name_user(self, create_user):

        respons_created, data = create_user
        token = respons_created.json()['accessToken']
        headers = {"Content-type": "application/json", "Authorization": f'{token}'}
        new_name_value = 'x' + respons_created.json()["user"]["name"]
        new_name = {"name": new_name_value}
        replace = requests.patch(Urls.REPLACE_DATA, json=new_name, headers=headers)

        assert replace.status_code == 200 and replace.json()['user']['name'] == new_name['name']

    @allure.title("Изменение имени неавторизованным пользаком")
    def test_not_auth_replacing_date_user(self, create_user):

        respons_created, data = create_user
        requests.post(Urls.CREATE_USER, data=data)
        headers = {"Content-type": "application/json"}
        new_name_value = 'x' + respons_created.json()["user"]["name"]
        new_name = {"name": new_name_value}
        replace = requests.patch(Urls.REPLACE_DATA, json=new_name, headers=headers)

        assert replace.status_code == 401 and TextAnswer.UNAUTHORIZED in replace.text
