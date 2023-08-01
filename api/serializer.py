# -*- coding:utf-8 -*-
# @Time     :2023/3/20 11:13 下午
# @Author   :CHNJX
# @File     :serializer.py
# @Desc     :序列化器
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from api.models import Project, Environment, Database, ProjectMember, InterfaceSuite, Interface, Testcase
from utils.validate_utils import ValidateDataIsExist


# 项目
class ProjectSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(help_text='项目创建者', label='项目创建者', read_only=True, slug_field='username')
    author_id = serializers.IntegerField(help_text='作者id', label='作者id', write_only=True,
                                         error_messages={'required': '作者不能为空'},
                                         validators=[ValidateDataIsExist('user')])

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


# 环境变量
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
                'error_messages': {'required': '环境名称不能为空'},
            },
            'project': {
                'error_messages': {'required': '环境名称不能为空'}
            }
        }
        model = Environment
        exclude = ('update_time',)


# 环境变量下拉选择
class EnvironmentSelectSerializer(serializers.ModelSerializer):
    # 只需要获取环境变量的id和name
    class Meta:
        model = Environment
        fields = ('id', 'name')


# 数据库
class DatabaseSerializer(serializers.ModelSerializer):
    # 读取列表时需要 所属项目和所属接口信息
    environment = serializers.SlugRelatedField(help_text='所属环境名称', label='所属项目名称',
                                               read_only=True, slug_field='name', )
    # 写的时候需要所属会写入所属项目id和所属接口id
    environment_id = serializers.IntegerField(help_text='所属项目id', label='所属环境id', write_only=True,
                                              error_messages={'required': '所属环境不能为空'},
                                              validators=[ValidateDataIsExist('environment')])

    class Meta:
        extra_kwargs = {
            'create_time': {
                'read_only': True,
                "format": "%Y年%m月%d日 %H:%M:%S"
            },
            'name': {
                'error_messages': {'required': '数据名称不能为空'}
            },
            'address': {
                'error_messages': {'required': '数据地址不能为空'}
            },
            'port': {
                'error_messages': {'required': '端口号不能为空'}
            },
            'user': {
                'error_messages': {'required': '用户名不能为空'}
            },
            'password': {
                'error_messages': {'required': '密码不能为空'}
            }
        }

        model = Database
        exclude = ('update_time',)


# 项目成员
class ProjectMemberSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(help_text='用户名称', label='用户名称', read_only=True, slug_field='username')
    user_id = serializers.IntegerField(help_text='所属项目id', label='所属项目id', write_only=True,
                                       validators=[ValidateDataIsExist('user')])
    # 读取列表时需要 所属项目和所属接口信息
    project = serializers.SlugRelatedField(help_text='所属项目名称', label='所属项目名称',
                                           read_only=True, slug_field='name', )
    # 写的时候需要所属会写入所属项目id和所属接口id
    project_id = serializers.IntegerField(help_text='所属项目id', label='所属项目id', write_only=True,
                                          validators=[ValidateDataIsExist('project')])

    def validate(self, attr: dict):
        user_id = attr.get('user_id')
        project_id = attr.get('project_id')
        count = ProjectMember.objects.filter(user_id=user_id, project_id=project_id).count()
        if count:
            raise serializers.ValidationError('项目成员已存在')
        return super().validate(attr)

    class Meta:
        extra_kwargs = {
            'create_time': {
                'read_only': True,
                "format": "%Y年%m月%d日 %H:%M:%S"
            },
            'project': {
                'error_messages': {'required': '项目不能为空'}
            },
            'user': {
                'error_messages': {'required': '用户不能为空'}
            }
        }

        model = ProjectMember
        exclude = ('update_time',)


# 获取项目成员列表
class PMMemberListSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(help_text='用户名称', label='用户名称', read_only=True, slug_field='username')
    user_id = serializers.IntegerField(help_text='所属项目id', label='所属项目id', read_only=True)

    class Meta:
        model = ProjectMember
        fields = ('user', 'user_id')


# 获取成员项目列表
class PMProjectListSerializer(serializers.ModelSerializer):
    # 读取列表时需要 所属项目和所属接口信息
    project = serializers.SlugRelatedField(help_text='所属项目名称', label='所属项目名称',
                                           read_only=True, slug_field='name', )
    # 写的时候需要所属会写入所属项目id和所属接口id
    project_id = serializers.IntegerField(help_text='所属项目id', label='所属项目id', read_only=True)

    class Meta:
        model = ProjectMember
        fields = ('project', 'project_id')


# 接口集
class InterfaceSuiteSerializer(serializers.ModelSerializer):
    project = serializers.SlugRelatedField(help_text='所属项目名称', label='所属项目名称',
                                           read_only=True, slug_field='name', )
    project_id = serializers.IntegerField(help_text='所属项目id', label='所属项目id', write_only=True,
                                          validators=[ValidateDataIsExist('project')],
                                          error_messages={"required": "所属项目不能为空"})

    def validate(self, attr: dict):
        name = attr.get('name')
        project_id = attr.get('project_id')
        count = InterfaceSuite.objects.filter(name=name, project_id=project_id).count()
        if count:
            raise serializers.ValidationError('该项目下与存在相同名称的接口集')
        return super().validate(attr)

    class Meta:
        extra_kwargs = {
            'create_time': {
                'read_only': True,
                "format": "%Y年%m月%d日 %H:%M:%S"
            },
            'name': {
                'error_messages': {'required': '环境名称不能为空'},
            },
            'project': {
                'error_messages': {'required': '环境名称不能为空'}
            }
        }
        model = InterfaceSuite
        exclude = ('update_time',)


# 接口集下拉列表数据
class InterfaceSuiteSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterfaceSuite
        fields = ('id', 'name')


# 接口序列器
class InterfaceSerializer(serializers.ModelSerializer):
    interface_suite = serializers.SlugRelatedField(help_text='所属接口集', label='所属接口集名称',
                                                   read_only=True, slug_field='name')
    interface_suite_id = serializers.IntegerField(help_text='所属接口集', label='所属接口集名称',
                                                  validators=[ValidateDataIsExist('interface_suite')],
                                                  error_messages={'required': '所属接口集不能为空'}, write_only=True
                                                  )

    class Meta:
        extra_kwargs = {
            'create_time': {
                'read_only': True,
                "format": "%Y年%m月%d日 %H:%M:%S"
            },
            'name': {
                'error_messages': {'required': '接口名称不能为空'}
            },
            'protocol': {
                'error_messages': {'required': '请求协议不能为空'}
            },
            'url': {
                'error_messages': {'required': '请求url不能为空'}
            }
        }
        model = Interface
        exclude = ('update_time',)

    def validate(self, attr: dict):
        count = Interface.objects.filter(name=attr.get('name'),
                                         interface_suite_id=attr.get('interface_suite_id')).count()
        if count:
            raise serializers.ValidationError('该接口集下与存在相同名称的接口')
        return super().validate(attr)


# 接口名称+id
class InterfaceNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interface
        fields = ('id', 'name')


# 获取接口集下的所有接口列表
class SuiteInterfaceListSerializer(serializers.ModelSerializer):
    interfaces = InterfaceNameSerializer(help_text='接口信息', label='接口信息', many=True, read_only=True)

    class Meta:
        model = InterfaceSuite
        fields = ('name', 'id', 'interfaces')


# 测试用例
class TestcaseSerializer(serializers.ModelSerializer):
    interface = serializers.SlugRelatedField(help_text="所属接口", label="所属接口", read_only=True, slug_field="name")
    interface_id = serializers.IntegerField(help_text="所属接口id", label="所属接口id",
                                            error_messages={"required": "所属接口不能为空"},
                                            validators=[ValidateDataIsExist('interface')])

    class Meta:
        extra_kwargs = {
            'create_time': {
                'read_only': True,
                "format": "%Y年%m月%d日 %H:%M:%S"
            },
            'name': {
                'error_messages': {'required': '用例名称不能为空'}
            }
        }

        model = Testcase
        exclude = ('update_time',)

