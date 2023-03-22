# -*- coding:utf-8 -*-
# @Time     :2023/1/15 4:40 下午
# @Author   :CHNJX
# @File     :env_transformation.py
# @Desc     :将数据库中的环境转换成对应格式


def generateSaveStr(data_list: list) -> str:
    res = ''
    for data in data_list:
        if data['key'] and data['value']:
            res += '(' + str(data['key']) + ',' + str(data['value']) + ');'
    return res


def getEnvHeaders(headers_str: str) -> list:
    herders_list = headers_str.strip(';').split(';')
    headers_res = []
    for i in herders_list:
        key_value = i.strip('(').strip(')').split(',')
        headers_res.append({'key': key_value[0], 'value': key_value[1]})
    return headers_res


def getEnvParams(params_str: str) -> list:
    """(key1,value1,备注1);(key2,value2,备注2);"""
    herders_list = params_str.strip(';').split(';')
    headers_res = []
    for i in herders_list:
        key_value = i.strip('(').strip(')').split(',')
        headers_res.append({'key': key_value[0], 'value': key_value[1], 'desc': key_value[2]})
    return headers_res


def getEnvHeaders2Hrun(headers_str: str) -> dict:
    if not headers_str:
        return None
    herders_list = headers_str.strip(';').split(';')
    headers_res = {}
    for i in herders_list:
        key_value = i.strip('(').strip(')').split(',')
        headers_res[key_value[0]] = key_value[1]
    return headers_res


def getEnvHeaders2List(headers_str: str) -> list:
    herders_list = headers_str.strip(';').split(';')
    headers_res = []
    for i in herders_list:
        headers_dict = {}
        key_value = i.strip('(').strip(')').split(',')
        headers_dict['key'] = key_value[0]
        headers_dict['value'] = key_value[1]
        headers_res.append(headers_dict)
    return headers_res


def getBaseUrl(protocol: str, host: str) -> str:
    return f'{protocol}://{host}'
