from django.test import TestCase


# Create your tests here.


def generate_testcase_request_data(interface_data: dict, testcase_data: dict):
    for key, value in interface_data.items():
        if key in ("json", "data", "params") and value:
            for param_name in value.keys():
                if testcase_data.get(param_name):
                    value[param_name] = testcase_data[param_name]
    return interface_data


interface = {
    "json": {},
    "params": {"page": "", "size": "{}"},
    "data": {}
}

testcase = {
    "page": "1",
    "size": 10
}

print(generate_testcase_request_data(interface, testcase))
