# Generated by Django 4.1.7 on 2023-08-02 00:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Interface',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')),
                ('name', models.CharField(help_text='接口名称', max_length=255, verbose_name='接口名称')),
                ('url', models.CharField(help_text='URL', max_length=255, verbose_name='URL')),
                ('protocol', models.IntegerField(choices=[(1, 'http'), (2, 'https')], help_text='请求协议', verbose_name='请求协议')),
                ('method', models.CharField(help_text='请求方法', max_length=20, verbose_name='请求方法')),
                ('json_data', models.TextField(blank=True, help_text='key1,value1;key2,value2;', verbose_name='json请求数据')),
                ('form_data', models.TextField(blank=True, help_text='key1,value1;key2,value2;', verbose_name='from表单数据')),
                ('query_data', models.TextField(blank=True, help_text='key1,value1;key2,value2;', verbose_name='query数据')),
                ('headers', models.TextField(blank=True, help_text='请求头', verbose_name='请求头')),
            ],
            options={
                'verbose_name': '接口',
                'verbose_name_plural': '接口',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')),
                ('name', models.CharField(help_text='项目名称', max_length=255, unique=True, verbose_name='项目名称')),
                ('description', models.TextField(blank=True, help_text='描述', verbose_name='描述')),
                ('author', models.ForeignKey(blank=True, help_text='项目创建人', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='项目创建人')),
            ],
            options={
                'verbose_name': '项目',
                'verbose_name_plural': '项目',
            },
        ),
        migrations.CreateModel(
            name='TestResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')),
                ('case_id', models.IntegerField(help_text='关联的测试用例', verbose_name='关联的测试用例')),
                ('start_time', models.DateTimeField(auto_now_add=True, help_text='测试执行开始时间', verbose_name='开始时间')),
                ('end_time', models.DateTimeField(auto_now=True, help_text='测试执行结束时间', verbose_name='结束时间')),
                ('result', models.BooleanField(blank=True, default=True, help_text='测试用例执行结果，True表示通过，False表示失败', verbose_name='测试结果')),
                ('response_content', models.TextField(blank=True, help_text='接口返回的响应内容', null=True, verbose_name='响应内容')),
                ('response_code', models.IntegerField(blank=True, help_text='接口返回的响应状态码', null=True, verbose_name='响应状态码')),
                ('response_headers', models.TextField(blank=True, help_text='接口返回的响应头', null=True, verbose_name='响应头')),
                ('duration', models.FloatField(blank=True, help_text='测试用例执行所花费的时间', null=True, verbose_name='执行时长')),
            ],
            options={
                'verbose_name': '用例结果',
                'verbose_name_plural': '用例结果',
            },
        ),
        migrations.CreateModel(
            name='Testcase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')),
                ('name', models.CharField(help_text='用例名称', max_length=25, verbose_name='用例名称')),
                ('description', models.TextField(blank=True, help_text='用例描述', verbose_name='用例描述')),
                ('input_data', models.TextField(blank=True, help_text='输入数据', verbose_name='输入数据')),
                ('is_gen', models.IntegerField(blank=True, default=1, help_text='是否已经生成用例 1:未生成 2：已生成', verbose_name='是否已经生成用例')),
                ('case_file_name', models.CharField(blank=True, help_text='用例文件名', max_length=50, verbose_name='用例文件名')),
                ('interface', models.ForeignKey(help_text='所属接口', on_delete=django.db.models.deletion.CASCADE, to='api.interface', verbose_name='所属接口')),
            ],
            options={
                'verbose_name': '用例',
                'verbose_name_plural': '用例',
            },
        ),
        migrations.CreateModel(
            name='ProjectMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')),
                ('project', models.ForeignKey(help_text='参与的项目', on_delete=django.db.models.deletion.CASCADE, to='api.project', verbose_name='项目')),
                ('user', models.ForeignKey(help_text='参与项目的系统用户', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '项目成员',
                'verbose_name_plural': '项目成员',
            },
        ),
        migrations.CreateModel(
            name='InterfaceSuite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')),
                ('name', models.CharField(help_text='接口名称', max_length=255, verbose_name='接口名称')),
                ('description', models.TextField(blank=True, help_text='描述', verbose_name='描述')),
                ('project', models.ForeignKey(help_text='所属项目', on_delete=django.db.models.deletion.CASCADE, to='api.project', verbose_name='所属项目')),
            ],
            options={
                'verbose_name': '接口集',
                'verbose_name_plural': '接口集',
            },
        ),
        migrations.AddField(
            model_name='interface',
            name='interface_suite',
            field=models.ForeignKey(default=1, help_text='所属项目', on_delete=django.db.models.deletion.CASCADE, related_name='interfaces', to='api.interfacesuite', verbose_name='所属项目'),
        ),
        migrations.CreateModel(
            name='Environment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')),
                ('name', models.CharField(help_text='环境名称', max_length=20, verbose_name='环境名称')),
                ('input_data', models.TextField(blank=True, default='', help_text='输入数据', verbose_name='输入数据')),
                ('headers', models.TextField(blank=True, default='', help_text='请求头：key1,value1;key2,value2;', verbose_name='请求头')),
                ('base_url', models.TextField(default='', help_text='请求域名', verbose_name='请求域名')),
                ('project', models.ForeignKey(help_text='所属项目', on_delete=django.db.models.deletion.CASCADE, to='api.project', verbose_name='所属项目')),
            ],
            options={
                'verbose_name': '环境变量',
                'verbose_name_plural': '环境变量',
            },
        ),
        migrations.CreateModel(
            name='Database',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')),
                ('name', models.CharField(help_text='数据库名称', max_length=20, verbose_name='数据库名称')),
                ('address', models.CharField(help_text='数据库地址', max_length=50, verbose_name='数据库地址')),
                ('port', models.CharField(help_text='端口', max_length=10, verbose_name='端口')),
                ('user', models.CharField(help_text='用户名', max_length=20, verbose_name='用户名')),
                ('password', models.CharField(help_text='密码', max_length=50, verbose_name='密码')),
                ('database_name', models.CharField(help_text='数据库名', max_length=50, verbose_name='数据库名')),
                ('environment', models.ForeignKey(help_text='所属环境变量', on_delete=django.db.models.deletion.CASCADE, to='api.environment', verbose_name='所属环境变量')),
            ],
            options={
                'verbose_name': '数据库',
                'verbose_name_plural': '数据库',
            },
        ),
        migrations.CreateModel(
            name='Assertion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')),
                ('assertion_type', models.CharField(help_text='断言方式：eq：equals、in：in、re：正则匹配、lt：less than、gt：greater thanschema: schema mach', max_length=20, verbose_name='断言方式')),
                ('expected_value', models.TextField(help_text='断言预期值', verbose_name='预期值')),
                ('actual_value', models.TextField(help_text='响应实际值表达式', verbose_name='实际值')),
                ('reason', models.CharField(blank=True, help_text='断言描述', max_length=50, null=True, verbose_name='断言描述')),
                ('testcase', models.ForeignKey(help_text='所属用例id', on_delete=django.db.models.deletion.CASCADE, to='api.testcase', verbose_name='所属用例')),
            ],
            options={
                'verbose_name': '断言',
                'verbose_name_plural': '断言',
            },
        ),
    ]
