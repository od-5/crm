# coding=utf-8
from django.conf.urls import patterns, url

__author__ = 'alexy'


urlpatterns = patterns(
    'api.views',
    url(r'^tasks/$', 'task_list', name='task_list'),
    url(r'^tasks/(?P<pk>[0-9]+)/$', 'task_detail', name='task_detail'),
    url(r'^tasks/surface/(?P<pk>[0-9]+)/$', 'tasksurface_detail', name='tasksurface_detail'),
    url(r'^tasks/surface/porch/(?P<pk>[0-9]+)/$', 'tasksurfaceporch_detail', name='tasksurfaceporch_detail'),
)
