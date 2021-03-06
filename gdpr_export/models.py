# coding=utf-8
from django.db import models


class GDPRExportField(models.FileField):
    include = {}
    exclude = {}

    def __init__(self, include=None, exclude=None, **kwargs):
        if include is None:
            include = {}
        if exclude is None:
            exclude = {}

        assert isinstance(include, dict) and isinstance(exclude, dict)

        self.include = include
        self.exclude = exclude
        super(GDPRExportField, self).__init__(**kwargs)
