# -*- coding:utf-8 -*-
# @Time     :2023/3/24 2:32 下午
# @Author   :CHNJX
# @File     :urls.py
# @Desc     :用户路由

from django.urls import path, re_path
from rest_framework_simplejwt.views import TokenObtainPairView

from user.views import *

urlpatterns = [
    path('register/', UserView.as_view({'post': 'create'})),
    # re_path(r'(?P<username>\w{6,20})/count/$', ListUserCountView.as_view({
    #     'get': 'count'
    # })),
    # re_path(r'(?P<email>^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$)/count/$',
    #         ListUserCountView.as_view({
    #             'get': 'count'
    #         })),

]

