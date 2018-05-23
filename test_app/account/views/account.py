# coding=utf-8
from rest_framework import viewsets

from ..models.account import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
