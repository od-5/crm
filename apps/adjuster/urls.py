# coding=utf-8
from django.conf.urls import patterns, url
from django.views.generic import ListView, CreateView, UpdateView
from apps.adjuster.ajax import adjuster_task_client

from apps.adjuster.models import Adjuster
from .views import AdjusterListView, AdjusterTaskListView

__author__ = 'alexy'

urlpatterns = patterns(
    'apps.adjuster.views',
    url(r'^$', AdjusterListView.as_view(), name='list'),
    url(r'^add/$', 'adjuster_add', name='add'),
    url(r'^task_add/$', 'adjuster_task_add', name='task-add'),
    url(r'^task/(?P<pk>\d+)/$', 'adjuster_task_update', name='task-update'),
    url(r'^task_list/$', AdjusterTaskListView.as_view(), name='task-list'),
    url(r'^(?P<pk>\d+)/$', 'adjuster_update', name='change'),
    url(r'^task_client_ajax/$', adjuster_task_client, name='task-client-ajax'),
)
