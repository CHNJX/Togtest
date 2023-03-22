# -*- coding:utf-8 -*-
# @Time     :2023/3/20 11:13 下午
# @Author   :CHNJX
# @File     :serializer.py
# @Desc     :序列化器
from rest_framework import serializers
from api.models import Project, Environment
from utils.validate_utils import ValidateDataIsExist


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        extra_kwargs = {
            'create_time': {
                'read_only': True,
                "format": "%Y年%m月%d日 %H:%M:%S"
            },
            'name': {
                'error_messages': {'required': '项目名称不能为空'}
            }
        }
        model = Project
        exclude = ('update_time',)


class EnvironmentSerializer(serializers.ModelSerializer):
    # 读取列表时需要 所属项目和所属接口信息
    project = serializers.SlugRelatedField(help_text='所属项目名称', label='所属项目名称',
                                           read_only=True, slug_field='name', )
    # 写的时候需要所属会写入所属项目id和所属接口id
    project_id = serializers.IntegerField(help_text='所属项目id', label='所属项目id', write_only=True,
                                          validators=[ValidateDataIsExist('project')])

    class Meta:
        extra_kwargs = {
            'create_time': {
                'read_only': True,
                "format": "%Y年%m月%d日 %H:%M:%S"
            },
            'name': {
                'error_messages': {'required': '环境名称不能为空'}
            },
            'project': {
                'error_messages': {'required': '环境名称不能为空'}
            }
        }
        model = Environment
        exclude = ('update_time',)


class EnvironmentSelectSerializer(serializers.ModelSerializer):
    # 只需要获取环境变量的id和name
    class Meta:
        model = Environment
        fields = ('id', 'name')