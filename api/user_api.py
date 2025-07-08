import requests
from data.data_url import DataUrl

class UserAPI:
    def __init__(self):
        self.base_url = DataUrl.BASE_URL

    def create_user(self, user_data):
        return requests.post(self.base_url + "/auth/register", json=user_data)

    def delete_user(self, token):
        headers = {"Authorization": token}
        return requests.delete(self.base_url + "/auth/user", headers=headers)
