# -*- coding:utf-8 -*-
# @Time     :2023/3/24 2:20 下午
# @Author   :CHNJX
# @File     :serializer.py
# @Desc     :用户序列化器


from django.contrib.auth.models import User
from rest_framework import serializers

# 因为JWT的序列化器只有登录  没有注册所以需要自己创建注册类 以及对应序列化器
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(TokenObtainPairSerializer, serializers.ModelSerializer):
    # 定义数据库没有的字段
    password_confirm = serializers.CharField(min_length=6, max_length=20, write_only=True)
    token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('username', 'id', 'email', 'password', 'token', 'password_confirm')
        extra_kwargs = {
            'password': {
                'min_length': 6,
                'max_length': 20,
                'write_only': True
            },
            'email': {
                'required': True,
                'allow_null': False,
                'allow_blank': False,
                'error_messages': {
                    'required': '邮箱不能为空'
                },
                'validators': [UniqueValidator(queryset=User.objects.all(), message='邮箱已存在')]
            }
        }

    def validate(self, attrs):
        # 判断密码和确认密码是否一致
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError('两次密码不一致')
        return attrs

    def create(self, validated_data):
        # 新增用户 只需要用户名、密码、邮箱
        user = User.objects.create_user(username=validated_data['username'], password=validated_data['password'],
                                        email=validated_data['email'])
        user.token = str(self.get_token(user).access_token)

        return user


class UserLoginSerializer(TokenObtainPairSerializer):
    # 重写序列化器  自定义登录后响应的内容
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        # data['refresh'] = str(refresh)
        data.pop('refresh')
        data.pop('access')
        data['token'] = str(refresh.access_token)

        # Add extra responses here
        data['username'] = self.user.username
        data['user_id'] = self.user.id
        return data
