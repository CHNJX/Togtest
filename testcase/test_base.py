import os

from api_driver.utils.service_logger import Logger
from api_driver.testcase_mixin import TestcaseMixin


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

    def replace_formal_list_2_act(self, formal_dict: list, act_dict: dict):
        for index, v in enumerate(formal_dict):
            if isinstance(v, str):
                formal_dict[index] = self.replace_formal_str_2_act(v, act_dict)
            elif isinstance(v, dict):
                self.replace_formal_dict_2_act(v, act_dict)
            elif isinstance(v, list):
                self.replace_formal_list_2_act(v, act_dict)
