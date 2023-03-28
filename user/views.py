from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from rest_framework import permissions
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet

from user.serializer import UserSerializer


class UserView(CreateModelMixin, GenericViewSet):
    permission_classes = [permissions.AllowAny]

    queryset = User.objects.all()
    serializer_class = UserSerializer
