from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    # 共用字段  id、创建时间、更新时间
    # auto_now_add 每次添加自动填入  auto_now 每次修改都会自动更新
    # id = models.AutoField(primary_key=True, verbose_name='项目主键', help_text='项目主键')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间', help_text='更新时间')

    class Meta:
        abstract = True  # 不会创建该表


class Project(BaseModel):
    name = models.CharField(max_length=255, verbose_name='项目名称', help_text='项目名称', unique=True)
    description = models.TextField(blank=True, verbose_name='描述', help_text='描述')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='项目创建人', help_text='项目创建人', null=True,blank=True)

    class Meta:
        verbose_name = '项目'
        verbose_name_plural = '项目'

    def __str__(self):
        return self.name


class Environment(BaseModel):
    name = models.CharField(max_length=20, verbose_name='环境名称', help_text='环境名称')
    input_data = models.TextField(verbose_name='输入数据', help_text='输入数据', blank=True, default='')
    headers = models.TextField(verbose_name='请求头', help_text='请求头：key1,value1;key2,value2;', blank=True, default='')
    project = models.ForeignKey('Project', on_delete=models.CASCADE, verbose_name='所属项目', help_text='所属项目')
    base_url = models.TextField(verbose_name='请求域名', help_text='请求域名', default='')

    class Meta:
        verbose_name = '环境变量'
        verbose_name_plural = '环境变量'

    def __str__(self):
        return self.name


class Database(BaseModel):
    name = models.CharField(max_length=20, verbose_name='数据库名称', help_text='数据库名称')
    address = models.CharField(max_length=50, verbose_name='数据库地址', help_text='数据库地址')
    port = models.CharField(max_length=10, verbose_name='端口', help_text='端口')
    user = models.CharField(max_length=20, verbose_name='用户名', help_text='用户名')
    password = models.CharField(max_length=50, verbose_name='密码', help_text='密码')
    database_name = models.CharField(max_length=50, verbose_name='数据库名', help_text='数据库名')
    environment = models.ForeignKey(Environment, on_delete=models.CASCADE, verbose_name='所属环境变量', help_text='所属环境变量')

    class Meta:
        verbose_name = '数据库'
        verbose_name_plural = '数据库'

    def __str__(self):
        return self.name


class InterfaceSuite(BaseModel):
    name = models.CharField(max_length=255, verbose_name='接口名称', help_text='接口名称')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='所属项目', help_text='所属项目')
    description = models.TextField(blank=True, verbose_name='描述', help_text='描述')

    class Meta:
        verbose_name = '接口集'
        verbose_name_plural = '接口集'

    def __str__(self):
        return self.name


class Interface(BaseModel):
    name = models.CharField(max_length=255, verbose_name='接口名称', help_text='接口名称')
    url = models.CharField(max_length=255, verbose_name='URL', help_text='URL')
    protocol = models.IntegerField(choices=((1, 'http'), (2, 'https')), verbose_name='请求协议', help_text='请求协议')
    method = models.CharField(max_length=20, verbose_name='请求方法', help_text='请求方法')
    json_data = models.TextField(verbose_name='json请求数据', help_text='key1,value1;key2,value2;', blank=True)
    form_data = models.TextField(verbose_name='from表单数据', help_text='key1,value1;key2,value2;', blank=True)
    query_data = models.TextField(verbose_name='query数据', help_text='key1,value1;key2,value2;', blank=True)
    headers = models.TextField(verbose_name='请求头', help_text='请求头', blank=True)
    interface_suite = models.ForeignKey(InterfaceSuite, on_delete=models.CASCADE, verbose_name='所属项目', help_text='所属项目',
                                        default=1, related_name='interfaces')

    class Meta:
        verbose_name = '接口'
        verbose_name_plural = '接口'

    def __str__(self):
        return self.name


class Testcase(BaseModel):
    name = models.CharField(max_length=25, verbose_name='用例名称', help_text='用例名称')
    description = models.TextField(blank=True, verbose_name='用例描述', help_text='用例描述')
    input_data = models.TextField(verbose_name='输入数据', help_text='输入数据', blank=True)
    is_gen = models.IntegerField(verbose_name="是否已经生成用例", help_text='是否已经生成用例 1:未生成 2：已生成', blank=True, default=1)
    case_file_name = models.CharField(max_length=50, verbose_name="用例文件名", help_text="用例文件名", blank=True)
    interface = models.ForeignKey(Interface, on_delete=models.CASCADE, verbose_name='所属接口', help_text='所属接口')

    class Meta:
        verbose_name = '用例'
        verbose_name_plural = '用例'

    def __str__(self):
        return self.name


class Assertion(BaseModel):
    assertion_type = models.CharField(max_length=20, verbose_name='断言方式',
                                      help_text='断言方式：json、re：正则匹配、'
                                                'schema: schema mach')
    expression = models.TextField(verbose_name='断言表达式', help_text='断言表达式')
    reason = models.CharField(max_length=50, verbose_name='断言描述', help_text='断言描述', null=True, blank=True)
    testcase = models.ForeignKey(Testcase, on_delete=models.CASCADE, verbose_name='所属用例', help_text='所属用例id')

    class Meta:
        verbose_name = '断言'
        verbose_name_plural = '断言'

    def __str__(self):
        return self.assertion_type


class TestResult(BaseModel):
    case_id = models.IntegerField(verbose_name='关联的测试用例', help_text='关联的测试用例')
    start_time = models.DateTimeField(auto_now_add=True, verbose_name='开始时间', help_text='测试执行开始时间')
    end_time = models.DateTimeField(auto_now=True, verbose_name='结束时间', help_text='测试执行结束时间')
    result = models.BooleanField(verbose_name='测试结果', help_text='测试用例执行结果，True表示通过，False表示失败', default=True, blank=True)
    response_content = models.TextField(blank=True, verbose_name='响应内容', help_text='接口返回的响应内容', null=True)
    response_code = models.IntegerField(blank=True, null=True, verbose_name='响应状态码', help_text='接口返回的响应状态码')
    response_headers = models.TextField(blank=True, verbose_name='响应头', help_text='接口返回的响应头', null=True)
    duration = models.FloatField(verbose_name='执行时长', help_text='测试用例执行所花费的时间', null=True, blank=True)

    class Meta:
        verbose_name = '用例结果'
        verbose_name_plural = '用例结果'

    def __str__(self):
        return f"Test Result for Test Case ID {self.case_id}"

    class Meta:
        verbose_name = '用例结果'
        verbose_name_plural = '用例结果'

    def __str__(self):
        return f"Test Result for Test Case ID {self.case_id}"


class ProjectMember(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户', help_text='参与项目的系统用户')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='项目', help_text='参与的项目')

    class Meta:
        verbose_name = '项目成员'
        verbose_name_plural = '项目成员'

    def __str__(self):
        return f"{self.user.username} in Project {self.project.name}"
