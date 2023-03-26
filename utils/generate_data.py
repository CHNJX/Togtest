# -*- coding:utf-8 -*-
# @Time     :2023/3/25 5:40 下午
# @Author   :CHNJX
# @File     :generate_data.py
# @Desc     :转换requests_data
from api.models import Interface, Environment


def convert_to_dict(data_str: str) -> dict:
    if data_str:
        return {key: value for key, value in [item.split(":") for item in data_str.strip(";").split(";")]}
    return {}


def generate_requests_data(interface_instance: Interface, env_instance: Environment) -> dict:
    url = interface_instance.url
    method = interface_instance.method
    headers = convert_to_dict(interface_instance.headers)
    json_data = convert_to_dict(interface_instance.json_data)
    form_data = convert_to_dict(interface_instance.form_data)
    query_data = convert_to_dict(interface_instance.query_data)
    form_data.update(env_instance.input_data)
    headers.update(convert_to_dict(env_instance.headers))
    base_url = env_instance.base_url
    request_data = {
        "method": method,
        "url": f"{base_url}{url}",
        "json": json_data,
        "data": form_data,
        "params": query_data,
        "headers": headers
    }
    return request_data


def generate_testcase_request_data(interface_data: dict, testcase_data: dict) -> dict:
    for key, value in interface_data.items():
        if key in ("json", "data", "params") and value:
            for param_name in value.keys():
                if testcase_data.get(param_name):
                    value[param_name] = testcase_data[param_name]
    return interface_data
