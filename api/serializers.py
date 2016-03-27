# coding=utf-8
from rest_framework import serializers
from apps.adjuster.models import AdjusterTask, AdjusterTaskSurface, AdjusterTaskSurfacePorch, SurfacePhoto
from apps.city.models import Porch
from core.models import User

__author__ = 'alexy'


class SurfacePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurfacePhoto
        field = {
            'id',
            'porch',
            'adjuster',
            'date',
            'image',
            'is_broken'
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'last_name',
            'first_name',
            'patronymic',
            'phone'
        )


class PorchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Porch
        fields = (
            'id',
            'number',
            'broken_shield',
            'broken_gib',
            'no_glass',
            'replace_glass',
            'against_tenants',
            'no_social_info'
        )


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdjusterTask
        fields = (
            'get_api_url',
            'id',
            '__unicode__',
            'date',
            'get_city_name',
            'get_surface_count',
            'get_porch_count',
            'get_type_display',
            'comment'
        )


class TaskSurfaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdjusterTaskSurface
        fields = (
            'id',
            'adjustertask',
            'surface',
            'get_address',
            'get_coord',
            'get_porch_count',
            'get_api_url'
        )


class TaskSurfacePorchSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdjusterTaskSurfacePorch
        fields = (
            'id',
            'is_closed',
        )
