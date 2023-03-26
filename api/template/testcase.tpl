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
        return self.http.req(**req_data)