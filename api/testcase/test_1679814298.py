import json

import pytest
from api.utils.http import Http
import allure


class Test1:
    def setup_method(self):
        self.http = Http()

    @allure.title("first")
    @pytest.mark.django_db(transaction=True)
    def test_1(self, get_test_result):
        req_data = {'method': 'GET', 'url': 'https://plan-test.ienjoys.com/api/v1/cleaning/pointTypes',
                    'json': {'pageSize': '10', 'page': '1'}, 'data': {}, 'params': {'pageSize': '10', 'page': '1'},
                    'headers': {'debug': 'True', 'userId': '3634555426785464790'}}
        # 计算执行时间
        resp = self.http.req(**req_data)
        response_content = json.dumps(resp['response_body'])
        response_code = resp['status_code']
        response_headers = resp['response_headers']

        get_test_result(1, response_content, response_code, response_headers)
        assert 1 == 1

