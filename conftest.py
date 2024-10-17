import pytest
import requests

from methods import Methods
from data import Urls


@pytest.fixture(scope='function')
def create_user():
    methods = Methods()
    data = methods.generate_user_data()
    response_post = requests.post(Urls.CREATE_USER, data=data)
    token = response_post.json()['accessToken']
    headers = {"Content-type": "application/json", "Authorization": f'{token}'}
    yield response_post, data
    requests.delete(Urls.DELETE_USER, headers=headers)
