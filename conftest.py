# # -*- coding:utf-8 -*-
# # @Time     :2023/3/26 3:06 下午
# # @Author   :CHNJX
# # @File     :conftest.py
# # @Desc     :保存测试结果
# import os
# import re
# from api.utils.testcase_utils import save_result
# import pytest
# from api.utils.testcase_utils import set_test_result
# from django.conf import settings
# from django.test.utils import setup_test_environment, teardown_test_environment
# from django.test.runner import DiscoverRunner as DjangoTestRunner
# import django
#
# from datetime import datetime
#
# # @pytest.fixture(scope='function')
# # def populate_users(django_db_setup, django_db_blocker):
# #     with django_db_blocker.unblock():
# #         project = Project.objects.all()
# #         yield project
# #
# #
# # @pytest.hookimpl(hookwrapper=True)
# # def pytest_runtest_makereport(item, call):
# #     outcome = yield
# #     set_test_result()
# #     rep = outcome.get_result()
# #     if rep.when == "call":
# #         if rep.passed:
# #             item.user_properties.append(("result", "passed"))
# #         else:
# #             item.user_properties.append(("result", "failed"))
#
#
# # @pytest.fixture(scope='function', autouse=True)
# # def save_test_result(request, pytestconfig, django_db_setup, django_db_blocker):
# #     with django_db_blocker.unblock():
# #         # 设置结果
# #         start_time = datetime.now()
# #         yield
# #         end_time = datetime.now()
# #         result = request.node.get_closest_marker("result")
# #         if result is not None:
# #             result = result.args[0]
# #             passed = result == "passed"
# #             duration = (end_time - start_time).total_seconds()
# #             case_id = int(request.node.name.split('_')[-1])
# #             with django_db_blocker.unblock():
# #                 TestResult.objects.filter(case_id=case_id).latest('create_time').update(
# #                     start_time=start_time,
# #                     end_time=end_time,
# #                     result=passed,
# #                     duration=duration,
# #                 )
# #
# #
# # @pytest.fixture(scope='class',autouse=True)
# # def get_test_result(django_db_setup, django_db_blocker):
# #     with django_db_blocker.unblock():
# #         return User.objects.get(id=4)
#
#
# # def pytest_terminal_summary(terminalreporter, exitstatus):
# #     # 获取测试结果
# #     results = terminalreporter.stats
# #     print("+++++++++++++++++++++++")
# #     print(results)
#
#
# # @pytest.mark.hookwrapper
# # def pytest_runtest_makereport(item, call):  # description取值为用例说明__doc__
# #     """获取测试结果、生成测试报告"""
# #     outcome = yield
# #     report = outcome.get_result()
# #     print("@@@@@@@@@@@@@@@@")
# #     print(report)
#
# @pytest.fixture(autouse=True)
# def enable_db_access_for_all_tests(db):
#     pass
#
#
# test_result = {}
#
#
# @pytest.hookimpl(hookwrapper=True, tryfirst=True)
# def pytest_runtest_makereport(item, call):
#     print('------------------------------------')
#
#     # 获取钩子方法的调用结果，返回一个result对象
#     out = yield
#     print('用例执行结果', out)
#
#     # 从钩子方法的调用结果中获取测试报告
#     report = out.get_result()
#     res = re.search('_(.*)?_', report.nodeid)
#     tc_id = res.group(1)
#     if test_result.get(tc_id):
#         if report.outcome == 'failed':
#             test_result[tc_id] = 'failed'
#     else:
#         test_result[tc_id] = report.outcome
#     print('测试报告：%s' % report)
#     print('步骤：%s' % report.when)
#     print('nodeid：%s' % report.nodeid)
#     print('description:%s' % str(item.function.__doc__))
#     print(('运行结果: %s' % report.outcome))
#
#
# def pytest_sessionfinish(session, exitstatus):
#     save_result(test_result)
