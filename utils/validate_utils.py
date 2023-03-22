# -*- coding:utf-8 -*-
# @Time     :2022/10/18 6:52 下午
# @Author   :CHNJX
# @File     :validate_utils.py
# @Desc     :自定义字段校验方法
from rest_framework import serializers

from api.models import Environment,Project


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

