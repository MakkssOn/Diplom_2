import requests
from data.data_url import DataUrl

class OrdersAPI:
    def __init__(self):
        self.base_url = DataUrl.BASE_URL

    def create_order(self, token, order_data):
        headers = {"Authorization": token}
        return requests.post(self.base_url + "/orders", headers=headers, json=order_data)

    def delete_order(self, token, order_id):
        headers = {"Authorization": token}
        return requests.delete(self.base_url + f"/orders/{order_id}", headers=headers)
