# -*- coding:utf-8 -*-
# @Time     :2023/3/26 11:33 上午
# @Author   :CHNJX
# @File     :testcase_utils.py
# @Desc     :测试用例执行
import os
import subprocess
from api.utils.template import Template


def execute_testcase(testcase_file: str):
    subprocess.call(f'pytest --ds=test.settings -v -s {testcase_file}', shell=True)


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
