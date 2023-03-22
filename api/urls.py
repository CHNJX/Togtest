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
urlpatterns = [
]

urlpatterns += router.urls
