# -*- coding:utf-8 -*-
# @Time     :2023/3/21 10:20 下午
# @Author   :CHNJX
# @File     :api_views.py
# @Desc     :项目视图
import json
import os
import time

from rest_framework import status, permissions
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet

from api.forms import TestDataUploadForm
from api.models import Assertion
from api.serializer import *
from api.utils.custom_json_response import JsonResponse
from api.utils.custom_pagination import PageNumberPagination
from api.utils.custom_view_set import CustomModelViewSet
from api.utils.http import Http
from api.utils.testcase_utils import execute_testcase, create_pytest_case

# 项目视图
from utils.database_conn import DatabaseConn
from utils.generate_data import generate_requests_data


class ProjectView(CustomModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    pagination_class = PageNumberPagination

    def destroy(self, request, *args, **kwargs):
        # 只有创建人才能进行删除
        instance: Project = self.get_object()
        if instance.author_id != request.user.id:
            return JsonResponse(data={}, msg='非创建人不能够删除项目', status=status.HTTP_403_FORBIDDEN)
        else:
            return super().destroy(request, *args, **kwargs)


# 环境变量视图
class EnvView(CustomModelViewSet):
    permission_classes = [permissions.AllowAny]

    queryset = Environment.objects.all()
    serializer_class = EnvironmentSerializer
    pagination_class = PageNumberPagination

    @action(methods=['GET'], detail=False)
    def tree_list(self, request, *args, **kwargs):
        """
        获取环境变量列表  name and id
        """
        qs = self.filter_queryset(self.get_queryset().filter(project_id=request.query_params['project_id']))
        serializer = self.get_serializer(qs, many=True)
        return JsonResponse(data=serializer.data, msg='成功', status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if self.action == 'tree_list':
            return EnvironmentSelectSerializer
        else:
            return super().get_serializer_class()


# 项目成员视图
class ProjectMemberView(CreateModelMixin, GenericViewSet):
    permission_classes = [permissions.AllowAny]

    queryset = ProjectMember.objects.all()
    serializer_class = ProjectMemberSerializer
    pagination_class = PageNumberPagination

    @action(methods=['delete'], detail=False)
    def delete_member(self, request, *args, **kwargs):
        """删除项目成员"""
        request_data = request.data
        qs = self.queryset.filter(project_id=request_data['project_id'], user_id=request_data['user_id'])
        serializer = self.get_serializer(qs)
        qs.delete()
        return JsonResponse(data=serializer.data, msg='删除成功', status=status.HTTP_204_NO_CONTENT)

    @action(methods=['GET'], detail=False)
    def member_list(self, request, *args, **kwargs):
        """根据项目id获取用户已列表 name + id"""
        qs = self.queryset.filter(project_id=request.query_params['project_id'])
        serializer = self.get_serializer(qs, many=True)
        return JsonResponse(data=serializer.data, msg='成功', status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False)
    def project_list(self, request, *args, **kwargs):
        """根据项目id获取用户已列表 name + id"""
        qs = self.queryset.filter(user_id=request.query_params['user_id'])
        serializer = self.get_serializer(qs, many=True)
        return JsonResponse(data=serializer.data, msg='成功', status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if self.action == 'member_list':
            return PMMemberListSerializer
        elif self.action == 'project_list':
            return PMProjectListSerializer
        else:
            return super().get_serializer_class()


# 数据库视图
class DatabaseView(CustomModelViewSet):
    permission_classes = [permissions.AllowAny]

    queryset = Database.objects.all()
    serializer_class = DatabaseSerializer

    @action(methods=['GET'], detail=False)
    def info(self, request, *args, **kwargs):
        qs = self.get_queryset().get(environment_id=request.query_params['env_id'])
        serializer = self.get_serializer(qs)
        return JsonResponse(data=serializer.data, msg='成功', status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=True)
    def execute(self, request, *args, **kwargs):
        database = self.get_object()
        database_config = {
            'host': database.address,
            'port': int(database.port),
            'user': database.user,
            'password': database.password,
            'database': database.database_name,
            'autocommit': True
        }
        sql_str = request.data['sql_str']
        dc = None
        try:
            dc = DatabaseConn(database_config)
            res = dc.excuse_sql(sql_str)
            return JsonResponse(data={'res': res}, msg='成功', status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse(data={'res': e.__str__()}, msg='执行失败', status=status.HTTP_400_BAD_REQUEST)
        finally:
            if dc:
                dc.close_conn()


# 接口集
class InterfaceSuiteView(CustomModelViewSet):
    permission_classes = [permissions.AllowAny]

    queryset = InterfaceSuite.objects.all()
    serializer_class = InterfaceSuiteSerializer
    pagination_class = PageNumberPagination

    # 获取下接口集拉选项数据
    @action(methods=['GET'], detail=False)
    def tree_list(self, request, *args, **kwargs):
        qs = self.filter_queryset(self.get_queryset().filter(project_id=request.query_params['project_id']))
        serializer = self.get_serializer(qs, many=True)
        return JsonResponse(data=serializer.data, msg='成功', status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False)
    def interface_list(self, request, *args, **kwargs):
        qs = self.filter_queryset(self.get_queryset().all())
        serializer = self.get_serializer(qs, many=True)
        return JsonResponse(data=serializer.data, msg='成功', status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if self.action == 'tree_list':
            return InterfaceSuiteSelectSerializer
        elif self.action == 'interface_list':
            return SuiteInterfaceListSerializer
        else:
            return super().get_serializer_class()


# 接口视图
class InterfaceView(CustomModelViewSet):
    permission_classes = [permissions.AllowAny]

    queryset = Interface.objects.all()
    serializer_class = InterfaceSerializer
    pagination_class = PageNumberPagination

    @action(methods=['GET'], detail=True)
    def debug(self, request, *args, **kwargs):
        interface = self.get_object()
        env_id = request.query_params.get('env_id')
        env = Environment.objects.get(id=int(env_id))
        request_data = generate_requests_data(interface, env)

        try:
            response = Http().req(**request_data)
            request = response['request']
            response['request'] = {
                "headers": request.headers._store,
                "url": request.url,
                "method": request.method,
                "body": request.body.decode('utf-8')
            }
            if response['status_code'] == 200:
                resp = response
            else:
                resp = response['text']
            return JsonResponse(data={"response": resp}, msg='成功', status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse(data={"error": e}, msg='请求失败', status=status.HTTP_400_BAD_REQUEST)


# 测试用例视图
class TestcaseView(CustomModelViewSet):
    permission_classes = [permissions.AllowAny]

    queryset = Testcase.objects.all()
    serializer_class = TestcaseSerializer
    pagination_class = PageNumberPagination

    def handle_upload_test_data(self, testcase, uploaded_file):
        """
        处理上传的测试数据文件
        """
        test_data_file = f"{testcase.id}.{uploaded_file.name.split('.')[-1]}"
        test_data_path = os.path.join('test_data', test_data_file)
        with open(test_data_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        testcase.is_gen = True
        testcase.test_data = test_data_file
        testcase.save()

    def create(self, request, *args, **kwargs):
        """
        创建测试用例
        """
        case_type = self.request.query_params.get('type')

        if case_type == 'ddt':
            return self._create_ddt_testcase(request)
        else:
            return self._create_standard_testcase(request)

    def _create_ddt_testcase(self, request):
        """
        处理 DDT 类型的测试用例创建
        """
        assertions_data = request.data.pop('assertions', [])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        testcase_data = serializer.validated_data

        # 创建测试用例
        testcase = Testcase.objects.create(**testcase_data)

        # 创建关联的断言
        Assertion.objects.bulk_create([
            Assertion(testcase=testcase, **json.loads(assertion_data))
            for assertion_data in assertions_data
        ])

        # 处理上传用例数据文件
        form = TestDataUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES.get('file')
            if uploaded_file:
                self.handle_upload_test_data(testcase, uploaded_file)

        return JsonResponse(serializer.data, msg='创建成功', status=status.HTTP_201_CREATED)

    def _create_standard_testcase(self, request):
        """
        处理标准类型的测试用例创建
        """
        assertions_data = request.data.pop('assertions', [])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        testcase_data = serializer.validated_data

        # 创建测试用例
        testcase = Testcase.objects.create(**testcase_data)

        # 创建关联的断言
        Assertion.objects.bulk_create([
            Assertion(testcase=testcase, **assertion_data)
            for assertion_data in assertions_data
        ])

        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['POST'], detail=True)
    def upload_test_data(self, request, *args, **kwargs):
        """
        上传测试数据文件
        """
        testcase = self.get_object()
        form = TestDataUploadForm(request.POST, request.FILES)

        if not form.is_valid():
            return JsonResponse(data={}, msg='上传失败，数据格式异常', status=status.HTTP_400_BAD_REQUEST)

        uploaded_file = request.FILES['file']
        self.handle_upload_test_data(testcase, uploaded_file)

        return JsonResponse(data={}, msg='上传成功', status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=True)
    def execute(self, request, *args, **kwargs):
        """执行测试用例"""
        testcase = self.get_object()
        # 断言数据
        assertions = self.get_serializer(testcase).data['assertion_set']
        # generate_assert_expression(assertions)
        testcase_dir = f"{os.path.dirname(os.path.dirname(__file__))}/testcase"
        # 判断是否已经生成过用例 生成过就直接运行
        if testcase.is_gen == 2:
            case_name = testcase.case_file_name
            if os.path.exists(f"{testcase_dir}/{case_name}"):
                execute_testcase(f"{testcase_dir}/{case_name}")
                return JsonResponse(data={}, msg='成功', status=status.HTTP_200_OK)
        env_instance = Environment.objects.get(id=request.query_params['env_id'])
        testcase_file = create_pytest_case(assertions, env_instance, testcase, testcase_dir)
        result = execute_testcase(testcase_file)
        return JsonResponse(data={}, msg=result, status=status.HTTP_200_OK)



