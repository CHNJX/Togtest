from api.testcase.test_base import TestBase
from api.utils.http import Http
import allure


class Test{{case}}(TestBase):
    def setup_class(self):
        self.http = Http()

    @allure.title("{{case_name}}")
    def test_{{case}}(self):
        self.logger.info("测试用例：{{case_name}}；描述: {{description}}")
        req_data = {{request_data}}
        res = self.http.req(**req_data)
        {% for assertion in assertions %}
        self.logger.info("断言描述：",{{assertion.reason}})
        self.logger.info("assert str(jsonpath(resp, '$..{{assertion.actual_value}}')[0]) == '{{assertion.expected_value}}'")
        {%- if assertion.assertion_type=='eq' -%}
        assert str(jsonpath(resp, '$..{{assertion.actual_value}}')[0]) == "{{assertion.expected_value}}"
        {% endif %}
        {% endfor %}

