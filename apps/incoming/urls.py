# coding=utf-8
from django.conf.urls import patterns, url
from .views import IncomingClientListView, IncomingTaskListView

__author__ = 'alexy'

urlpatterns = patterns(
    'apps.incoming.views',
    url(r'^$', IncomingClientListView.as_view(), name='list'),
    url(r'^add/$', 'incomingclient_add', name='add'),
    url(r'^(?P<pk>\d+)/$', 'incomingclient_update', name='update'),
    url(r'^task/$', IncomingTaskListView.as_view(), name='task-list'),
    url(r'^task/add/$', 'incomingtask_add', name='task-add'),
    url(r'^task/(?P<pk>\d+)/$', 'incomingtask_update', name='task-update'),
)

