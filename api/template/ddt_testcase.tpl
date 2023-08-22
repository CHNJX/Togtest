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
        {% if assertion.assertion_type == 'json' %}
        assert_data = self.get_assert_data('{{assertion.expression}}',res,test_data,'json')
        self.logger.info(f'断言描述：{self.replace_formal_str_2_act("{{assertion.reason}}", test_data)}')
        self.logger.info(f'assert {assert_data["expect_expression"]} == {assert_data["actual"]}')
        assert assert_data['result']
        {% endif %}
        {% endfor %}
