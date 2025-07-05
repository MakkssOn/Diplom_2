import requests
from data.data_url import DataUrl

class IngredientsAPI:
    def get_ingredients(self):
        return requests.get(DataUrl.BASE_URL + "/ingredients")
