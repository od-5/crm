# coding=utf-8
from django.contrib import admin

from .models import Setup

class SetupAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'email')


admin.site.register(Setup, SetupAdmin)
