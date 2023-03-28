import json

import pytest
from api.utils.http import Http
import allure
from django.contrib.auth.models import User


class Test1:
    def setup_method(self):
        self.http = Http()

    @allure.title("first")
    @pytest.mark.django_db(transaction=True)
    def test_1(self,populate_users):
        req_data = {'method': 'GET', 'url': 'https://plan-test.ienjoys.com/api/v1/cleaning/pointTypes',
                    'json': {'pageSize': '10', 'page': '1'}, 'data': {}, 'params': {'pageSize': '10', 'page': '1'},
                    'headers': {'debug': 'True', 'userId': '3634555426785464790'}}
        # 计算执行时间
        resp = self.http.req(**req_data)

        assert 1 == 1

    @pytest.mark.django_db
    def test_users(self):
        assert 1 == 2