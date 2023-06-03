from typing import Any, Optional
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserChangeForm, UserCreationForm
from .models import *


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('phone_number', 'email', 'full_name')
    list_filter = ('is_admin',)

    fieldsets = (
        (None, {'fields': ('email', 'password',
         'phone_number', 'full_name', 'last_login')}),
        ('permission', {'fields': ('is_active',
         'is_admin', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {'fields': ('email', 'phone_number',
         'full_name', 'password1', 'password2')}),
    )

    readonly_fields = ('last_login', )

    search_fields = ('email',)
    ordering = ('full_name',)
    filter_horizontal = ('groups', 'user_permissions')

    def get_form(self, request, obj, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            form.base_fields['is_superuser'].disabled = True
        return form


# admin.site.unregister(Group)
admin.site.register(User, UserAdmin)


class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'code', 'created')


admin.site.register(OtpCode, OtpCodeAdmin)
