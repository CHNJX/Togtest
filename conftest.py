# -*- coding:utf-8 -*-
# @Time     :2023/3/26 3:06 下午
# @Author   :CHNJX
# @File     :conftest.py
# @Desc     :保存测试结果

import pytest
from django.conf import settings
from django.test.utils import setup_test_environment, teardown_test_environment
from django.test.runner import DiscoverRunner as DjangoTestRunner
import django

from datetime import datetime
from api.models import TestResult, Testcase


@pytest.fixture(scope='session', autouse=True)
def django_db_setup():
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test_db.sqlite3',
    }

@pytest.fixture(scope='session', autouse=True)
def django_test_environment():
    # 初始化Django
    settings.DEBUG = False
    django.setup()
    try:
        setup_test_environment()
    except RuntimeError:
        teardown_test_environment()
        setup_test_environment()
    runner = DjangoTestRunner()
    runner.teardown_test_environment()
    runner.setup_test_environment()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call":
        if rep.passed:
            item.user_properties.append(("result", "passed"))
        else:
            item.user_properties.append(("result", "failed"))


@pytest.fixture(scope='function', autouse=True)
def save_test_result(request, pytestconfig, django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        # 设置结果
        start_time = datetime.now()
        yield
        end_time = datetime.now()
        result = request.node.get_closest_marker("result")
        if result is not None:
            result = result.args[0]
            passed = result == "passed"
            duration = (end_time - start_time).total_seconds()
            case_id = int(request.node.name.split('_')[-1])
            with django_db_blocker.unblock():
                TestResult.objects.filter(case_id=case_id).latest('create_time').update(
                    start_time=start_time,
                    end_time=end_time,
                    result=passed,
                    duration=duration,
                )


@pytest.fixture(scope='function')
def get_test_result(django_db_setup, django_db_blocker):
    def _get_test_result(case_id, response_content, response_code, response_headers):
        with django_db_blocker.unblock():
            r = TestResult.objects.create(
                case_id=case_id,
                response_content=response_content,
                response_code=response_code,
                response_headers=response_headers,
            )
            r.save()

    return _get_test_result


