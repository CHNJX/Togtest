# -*- coding:utf-8 -*-
# @Time     :2023/3/26 11:33 上午
# @Author   :CHNJX
# @File     :testcase_utils.py
# @Desc     :测试用例执行
import os
import re
import time

from api.models import Project, TestResult, Environment, Testcase, Assertion
from api.utils.template import Template
from api_driver.api_driver import ApiDriver

from utils.generate_data import generate_requests_data, convert_to_dict, generate_testcase_request_data

abs_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + '/report'


def execute_testcase(testcase_file: str):
    res = re.search('_(.*)?_', testcase_file)
    tc_id = res.group(1)
    ad = ApiDriver()
    res = ad.run_tests(testcase_file)
    ad.generate_html_report(res, f'{abs_dir}/{tc_id}.html')
    save_result(tc_id, res)


def save_result(case_id: int, result: dict):
    res = True
    if result['fail_count']:
        res = False
    TestResult.objects.update_or_create(case_id=case_id, result=res)


def write(content, file_path):
    """
    将内容写入文档中
    :param content:  要写入的内容
    :param file_path: 文件路径（不存在则会进行创建）
    :return: None
    """
    dir_ = os.path.dirname(file_path)
    if not os.path.exists(dir_):
        os.makedirs(dir_)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)


def generate_testcase(testcase_data, file_path):
    template = Template()
    if testcase_data['test_data_file']:
        content = template.get_content('ddt_testcase.tpl', **testcase_data)
    else:
        content = template.get_content('testcase.tpl', **testcase_data)
    write(content, file_path)


def generate_assert_expression(assertions):
    for assertion in assertions:
        if assertion['assertion_type'] == 'json':
            assertion_list = assertion['expression'].split(' ')
            assertion_list[0] = f'jsonpath(res, "{assertion_list[0]}")[0]'
            assertion['expression'] = ' '.join(assertion_list)


def create_pytest_case(assertions: Assertion, env_instance: Environment, testcase: Testcase, testcase_dir: str):
    interface_instance = testcase.interface
    # 拿到接口的请求数据
    interface_data = generate_requests_data(interface_instance, env_instance)
    # 转换用例请求参数
    testcase_data_dict = convert_to_dict(testcase.input_data)
    request_data = generate_testcase_request_data(interface_data, testcase_data_dict)
    # 生成测试用例
    case_file_name = f"{testcase.id}_{str(int(time.time()))}.py"
    testcase_data = {
        "case": testcase.id,
        "case_name": testcase.name,
        "description": testcase.description,
        "request_data": request_data,
        "assertions": assertions,
        "test_data_file": testcase.test_data
    }
    testcase_file = f"{testcase_dir}/test_{case_file_name}"
    generate_testcase(testcase_data, testcase_file)
    testcase.is_gen = 2
    testcase.case_file_name = f"test_{case_file_name}"
    testcase.save()
    return testcase_file


