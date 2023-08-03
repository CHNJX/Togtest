from testcase.test_base import TestBase
from api.utils.http import Http
import allure
from jsonpath import jsonpath


class Test{{case}}(TestBase):
    def setup_class(self):
        self.http = Http()

    @allure.title("{{case_name}}")
    def test_{{case}}(self):
        self.logger.info("测试用例：{{case_name}}；描述: {{description}}")
        req_data = {{request_data}}
        res = self.http.req(**req_data)
        {% for assertion in assertions %}
        self.logger.info('断言描述：{{assertion.reason}}')
        self.logger.info('assert {{assertion.expression}}')
        {% if assertion.assertion_type == 'json' %}
        assert {{assertion.expression}}
        {% endif %}
        {% endfor %}

