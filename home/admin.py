from django.contrib import admin
from .models import *


class Admin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    raw_id_fields = ('category',)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'is_sub')


admin.site.register(Product, Admin)
admin.site.register(Category, CategoryAdmin)
