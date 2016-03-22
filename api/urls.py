# coding=utf-8
from django.conf.urls import patterns, url

__author__ = 'alexy'


urlpatterns = patterns(
    'api.views',
    url(r'^tasks/$', 'task_list', name='task_list'),
    url(r'^tasks/(?P<pk>[0-9]+)/$', 'adjustertask_detail', name='adjustertask_detail'),
    url(r'^tasks/surface/(?P<pk>[0-9]+)/$', 'adjustertasksurface_detail', name='adjustertasksurface_detail'),
)
