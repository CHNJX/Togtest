# -*- coding:utf-8 -*-
# @Time     :2023/3/21 10:29 下午
# @Author   :CHNJX
# @File     :urls.py
# @Desc     :api urls
from rest_framework import routers

from . import api_views

router = routers.SimpleRouter()
router.register(r'project', api_views.ProjectView)
router.register(r'env', api_views.EnvView)
router.register(r'pm', api_views.ProjectMemberView)
router.register(r'database', api_views.DatabaseView)
router.register(r'interface_suite', api_views.InterfaceSuiteView)
router.register(r'interface', api_views.InterfaceView)
router.register(r'testcase',api_views.TestcaseView)
urlpatterns = [
]

urlpatterns += router.urls
