# coding=utf-8
from django.conf.urls import patterns, url
from apps.adjustertask.ajax import adjuster_task_client, adjuster_get_area_streets
from .views import AdjusterTaskListView, TaskArchiveListView

__author__ = 'alexy'

urlpatterns = patterns(
    'apps.adjustertask.views',
    url(r'^$', AdjusterTaskListView.as_view(), name='list'),
    url(r'^archive/$', TaskArchiveListView.as_view(), name='archive'),
    url(r'^c_add/$', 'adjuster_c_task', name='add'),
    url(r'^a_add/$', 'adjuster_a_task', name='a_add'),
    url(r'^r_add/$', 'adjuster_r_task', name='r_add'),

    # url(r'^add/$', 'adjuster_task_add', name='add'),
    # url(r'^simple_task_add/$', 'adjuster_simple_task_add', name='simple_add'),
    url(r'^task/(?P<pk>\d+)/$', 'adjuster_task_update', name='update'),

    url(r'^task_client_ajax/$', adjuster_task_client, name='client-ajax'),
    url(r'^task_area_ajax/$', adjuster_get_area_streets, name='area-ajax'),
)
