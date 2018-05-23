# coding=utf-8
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils import timezone
from django.utils.timezone import now

from gdpr_export.models import GDPRExportField


def account_avatar_path(user, filename):
    return 'avatars/{}'.format(user.id)


def gdpr_data_path(user, filename):
    return 'gdpr    /{}'.format(user.id)


class ModifiedField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        value = now()
        setattr(model_instance, self.attname, value)
        return value


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        max_length=255,
        unique=True,
        help_text=(
            'Required. 255 characters or fewer. '
            'Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': 'A user with that username already exists.',
        },
    )
    created = models.DateTimeField(editable=False, default=now)
    modified = ModifiedField(editable=False, default=now)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(
        upload_to=account_avatar_path,
        null=True,
        blank=True
    )
    last_activity = models.DateTimeField(editable=False, default=timezone.now)
    gdpr_data = GDPRExportField(upload_to=gdpr_data_path, blank=True, null=True)

    def get_full_name(self):
        full_name = super(User, self).get_full_name()
        if not full_name:
            return self.username
        return full_name
