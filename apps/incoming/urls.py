# coding=utf-8
from django.conf.urls import patterns, url
from .views import IncomingClientListView, IncomingTaskListView
from .ajax import reassign_manager, get_available_manager_list, get_contact_list, get_incomingclient_info, \
    ajax_task_add, get_incomingtask_info, ajax_task_update

__author__ = 'alexy'

urlpatterns = patterns(
    'apps.incoming.views',
    url(r'^$', IncomingClientListView.as_view(), name='list'),
    url(r'^add/$', 'incomingclient_add', name='add'),
    url(r'^(?P<pk>\d+)/$', 'incomingclient_update', name='update'),
    url(r'^(?P<pk>\d+)/manager/history/$', 'incomingclientcontact_history', name='history'),
    url(r'^(?P<pk>\d+)/contact/$', 'incomingclientcontact_list', name='contact-list'),
    url(r'^(?P<pk>\d+)/contact/add/$', 'incomingclientcontact_add', name='contact-add'),
    url(r'^contact/(?P<pk>\d+)/$', 'incomingclientcontact_update', name='contact-update'),
    url(r'^task/$', IncomingTaskListView.as_view(), name='task-list'),
    url(r'^task/add/$', 'incomingtask_add', name='task-add'),
    url(r'^task/ajax-add/$', ajax_task_add, name='ajax-task-add'),
    url(r'^task/ajax-update/$', ajax_task_update, name='ajax-task-update'),
    url(r'^task/(?P<pk>\d+)/$', 'incomingtask_update', name='task-update'),
    url(r'^reassign-manager/$', reassign_manager, name='reassign-manager'),
    url(r'^get_available_manager_list/$', get_available_manager_list, name='get_available_manager_list'),
    url(r'^get_contact_list/$', get_contact_list, name='get_contact_list'),
    url(r'^get_incomingclient_info/$', get_incomingclient_info, name='get_incomingclient_info'),
    url(r'^get_incomingtask_info/$', get_incomingtask_info, name='get_incomingtask_info'),
)
