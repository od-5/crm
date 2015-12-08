# coding=utf-8
from django.contrib import admin
from .models import City, Area, ConstructionType, Surface


class AreaInline(admin.TabularInline):
    model = Area
    extra = 1


class ConstructionTypeInline(admin.TabularInline):
    model = ConstructionType
    extra = 1


class CityAdmin(admin.ModelAdmin):
    inlines = [
        AreaInline,
        ConstructionTypeInline
    ]

admin.site.register(City, CityAdmin)
admin.site.register(Surface)