# coding=utf-8
from rest_framework import serializers
from apps.adjuster.models import AdjusterTask, AdjusterTaskSurface, AdjusterTaskSurfacePorch

__author__ = 'alexy'


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdjusterTask
        fields = (
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
            'get_porch_count'
        )


class TaskSurfacePorchSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdjusterTaskSurfacePorch
        fields = (
            'id',
            'adjustertasksurface',
            'porch',
            'porch_number',
            'broken_shield',
            'broken_gib',
            'no_glass',
            'replace_glass',
            'against_tenants',
            'no_social_info'
        )
