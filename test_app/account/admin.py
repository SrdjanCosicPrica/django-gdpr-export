# coding=utf-8
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.utils.safestring import mark_safe

from gdpr_export.core import export_data
from .models.account import User
from .models.foreign_keys import ForeignKeyModel, FKSetModel
from .models.m2m import ManyToManyModel, M2MSetModel


class EmailRequiredMixin:
    def __init__(self, *args, **kwargs):
        super(EmailRequiredMixin, self).__init__(*args, **kwargs)
        # make user email field required
        self.fields['email'].required = True


class MyUserCreationForm(EmailRequiredMixin, UserCreationForm):
    pass


def export_user_data(modeladmin, request, queryset):
    for obj in queryset.all():
        export_data(obj)


class FKSetInline(admin.TabularInline):
    model = FKSetModel
    extra = 0


class ForeignKeyInline(admin.TabularInline):
    model = ForeignKeyModel
    extra = 0


class ManyToManyInline(admin.TabularInline):
    model = ManyToManyModel.user.through
    extra = 0


class M2MSetInline(admin.TabularInline):
    model = M2MSetModel.user.through
    extra = 0


class MyUserAdmin(UserAdmin):
    add_form = MyUserCreationForm
    fieldsets = UserAdmin.fieldsets + (
        ('Avatar', {'fields': ('avatar', 'avatar_preview')}),
        ('GDPR', {'fields': ('gdpr_data',)}),
    )
    readonly_fields = ('avatar_preview', 'last_activity',)

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

    actions = [export_user_data]
    inlines = [FKSetInline, ForeignKeyInline, ManyToManyInline, M2MSetInline]

    def avatar_preview(self, obj):
        if obj.avatar:
            return mark_safe('<img src="{}"/>'.format(obj.avatar.url))
        return None


admin.site.register(User, MyUserAdmin)
admin.site.register(ForeignKeyModel)
admin.site.register(FKSetModel)
admin.site.register(ManyToManyModel)
admin.site.register(M2MSetModel)
