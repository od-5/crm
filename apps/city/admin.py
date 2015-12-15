# coding=utf-8
from django.contrib import admin
from .models import City, Area, ConstructionType, Surface, Porch, Street

__author__ = 'alexy'


class AreaInline(admin.TabularInline):
    model = Area
    extra = 1


class StreetInline(admin.TabularInline):
    model = Street
    extra = 1


class PorchInline(admin.StackedInline):
    model = Porch
    extra = 1


class ConstructionTypeInline(admin.TabularInline):
    model = ConstructionType
    extra = 1


class CityAdmin(admin.ModelAdmin):
    inlines = [
        AreaInline,
        StreetInline,
        ConstructionTypeInline
    ]

class SurfaceAdmin(admin.ModelAdmin):
    list_display = ('city', 'street', 'house_number')
    inlines = [
        PorchInline,
    ]

admin.site.register(City, CityAdmin)
admin.site.register(Surface, SurfaceAdmin)
