import pytest
import yaml

from testcase.test_base import TestBase
from api.utils.http import Http
import allure
from jsonpath import jsonpath


class Test{{case}}(TestBase):
    def setup_class(self):
        self.http = Http()

    @allure.title("{{case_name}}")
    @pytest.mark.parametrize('test_data', yaml.safe_load(open('test_data/{{test_data_file}}', encoding='utf-8')))
    def test_{{case}}(self,test_data):
        self.logger.info("测试用例：{{case_name}}；描述: {{description}}")
        req_data = self.replace_formal_dict_2_act({{request_data}},test_data)
        res = self.http.req(**req_data)
        {% for assertion in assertions %}
        self.logger.info('断言描述：{{assertion.reason}}')
        self.logger.info('assert {{assertion.expression}}')
        {% if assertion.assertion_type == 'json' %}
        assert self.get_assert_res({{assertion.expression}},res,test_data,'json')
        {% endif %}
        {% endfor %}
