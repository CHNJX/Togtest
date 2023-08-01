import json

import pytest
from api.utils.http import Http
import allure


class Test1:
    def setup_method(self):
        self.http = Http()

    def test_1(self,transactional_db):
        req_data = {'method': 'GET', 'url': 'https://plan-test.ienjoys.com/api/v1/cleaning/pointTypes',
                    'json': {'pageSize': '10', 'page': '1'}, 'data': {}, 'params': {'pageSize': '10', 'page': '1'},
                    'headers': {'debug': 'True', 'userId': '3634555426785464790'}}
        # 计算执行时间
        resp = self.http.req(**req_data)

        assert 1 == 1

    def test_users(self,transactional_db):
        assert 1 == 2