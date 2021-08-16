# coding=utf-8
from django.urls import include, path, re_path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import *

__author__ = 'alexy'

app_name = 'api'

urlpatterns = [
    re_path(r'^$', api_root, name='index'),
    re_path(r'^tasks/$', task_list, name='task_list'),
    # re_path(r'^tasks/$', 'task_list', name='task_list'),
    # re_path(r'^tasks/(?P<pk>[0-9]+)/$', 'task_detail', name='task_detail'),
    re_path(r'^porch/(?P<pk>[0-9]+)/$', porch_update, name='porch_update'),
    re_path(r'^photo/$', photo_add, name='photo_add'),
    # re_path(r'^tasks/surface/(?P<pk>[0-9]+)/$', 'tasksurface_detail', name='tasksurface_detail'),
    re_path(r'^tasks/surface/porch/(?P<pk>[0-9]+)/$', tasksurfaceporch_detail, name='tasksurfaceporch_detail'),
]

# Format suffixes
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])
