# coding=utf-8
from django.conf.urls import patterns, url
from apps.adjustertask.ajax import adjuster_task_client, adjuster_task_remove, adjuster_get_area_streets
from .views import AdjusterTaskListView

__author__ = 'alexy'

urlpatterns = patterns(
    'apps.adjustertask.views',
    url(r'^$', AdjusterTaskListView.as_view(), name='list'),
    url(r'^task_add/$', 'adjuster_task_add', name='add'),
    url(r'^simple_task_add/$', 'adjuster_simple_task_add', name='simple_add'),
    url(r'^task/(?P<pk>\d+)/$', 'adjuster_task_update', name='update'),
    url(r'^task_remove/$', adjuster_task_remove, name='remove'),

    url(r'^task_client_ajax/$', adjuster_task_client, name='client-ajax'),
    url(r'^task_area_ajax/$', adjuster_get_area_streets, name='area-ajax'),
)
