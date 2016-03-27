# coding=utf-8
from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

__author__ = 'alexy'


urlpatterns = patterns(
    'api.views',
    url(r'^$', 'api_root', name='index'),
    url(r'^tasks/$', 'task_list', name='task_list'),
    # url(r'^tasks/$', 'task_list', name='task_list'),
    # url(r'^tasks/(?P<pk>[0-9]+)/$', 'task_detail', name='task_detail'),
    url(r'^porch/(?P<pk>[0-9]+)/$', 'porch_update', name='porch_update'),
    url(r'^photo/$', 'photo_add', name='photo_add'),
    # url(r'^tasks/surface/(?P<pk>[0-9]+)/$', 'tasksurface_detail', name='tasksurface_detail'),
    url(r'^tasks/surface/porch/(?P<pk>[0-9]+)/$', 'tasksurfaceporch_detail', name='tasksurfaceporch_detail'),
)

# Format suffixes
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])