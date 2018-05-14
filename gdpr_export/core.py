# coding=utf-8
from django.db import models


def export_data(object):
    assert isinstance(object, models.Model)

    for field in object._meta.get_fields():
        pass
