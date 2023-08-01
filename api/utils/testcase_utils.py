# -*- coding:utf-8 -*-
# @Time     :2023/3/26 11:33 上午
# @Author   :CHNJX
# @File     :testcase_utils.py
# @Desc     :测试用例执行
import os
import re
import subprocess
from httprunner import HttpRunner
from api.models import Project, TestResult
from api.utils.template import Template
import pytest
from api_driver.api_driver import ApiDriver

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
    content = template.get_content('testcase.tpl', **testcase_data)
    write(content, file_path)


def set_test_result():
    project = Project.objects.all()
    print('')
