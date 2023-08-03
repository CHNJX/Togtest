# -*- coding:utf-8 -*-
# @Time     :2022/10/18 6:52 下午
# @Author   :CHNJX
# @File     :validate_utils.py
# @Desc     :自定义字段校验方法
from django.contrib.auth.models import User
from rest_framework import serializers

from api.models import Environment, Project, InterfaceSuite, Interface


class ValidateDataIsExist:

    def __init__(self, model_name: str):
        """

        :param model_name: 需要校验字段对应的模型名称
        """
        self.model_name = model_name

    def __call__(self, pk):
        if self.model_name == 'project':
            if not Project.objects.filter(id=pk).exists():
                raise serializers.ValidationError('该项目不存在')
        elif self.model_name == 'user':
            if not User.objects.filter(id=pk).exists():
                raise serializers.ValidationError('该用户不存在')
        elif self.model_name == 'environment':
            if not User.objects.filter(id=pk).exists():
                raise serializers.ValidationError('该环境不存在')
        elif self.model_name == 'interface_suite':
            if not InterfaceSuite.objects.filter(id=pk).exists():
                raise serializers.ValidationError('该接口集不存在')
        elif self.model_name == 'interface':
            if not Interface.objects.filter(id=pk).exists():
                raise serializers.ValidationError('该接口不存在')
        elif self.model_name == 'testcase':
            if not Interface.objects.filter(id=pk).exists():
                raise serializers.ValidationError('该用例不存在')

