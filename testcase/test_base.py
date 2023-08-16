import os

from api_driver.utils.service_logger import Logger
from api_driver.testcase_mixin import TestcaseMixin
from jsonpath import jsonpath


class TestBase(TestcaseMixin):
    base_dir = os.path.join(os.path.dirname(__file__), '..')
    logger = Logger.getLogger("testcase", base_dir)

    def replace_formal_str_2_act(self, formal_str: str, act_dict: dict):
        if formal_str.startswith('${') and formal_str.endswith('}'):
            key = formal_str[2:len(formal_str) - 1]
            return act_dict[key]
        return formal_str

    def replace_formal_dict_2_act(self, formal_dict: dict, act_dict: dict):
        for k, v in formal_dict.items():
            if isinstance(v, str):
                formal_dict[k] = self.replace_formal_str_2_act(v, act_dict)
            elif isinstance(v, dict):
                self.replace_formal_dict_2_act(v, act_dict)
            elif isinstance(v, list):
                self.replace_formal_list_2_act(v, act_dict)
        return formal_dict

    def replace_formal_list_2_act(self, formal_dict: list, act_dict: dict):
        for index, v in enumerate(formal_dict):
            if isinstance(v, str):
                formal_dict[index] = self.replace_formal_str_2_act(v, act_dict)
            elif isinstance(v, dict):
                self.replace_formal_dict_2_act(v, act_dict)
            elif isinstance(v, list):
                self.replace_formal_list_2_act(v, act_dict)

    def get_assert_res(self, assertion_expression, res, act_data, assert_type):
        expression = ''
        if assert_type == 'json':
            assertion_list = assertion_expression.split(' ')
            for index, ass in enumerate(assertion_list):
                assertion_list[index] = str(self.replace_formal_str_2_act(ass, act_data))
            assertion_list[0] = str(jsonpath(res, assertion_list[0])[0])
            expression = ' '.join(assertion_list)

        result = eval(expression)
        return result
