# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.urls import include, path, re_path
from apps.incoming.data_import import client_list_import
from .views import *
from .ajax import reassign_manager, get_available_manager_list, get_contact_list, get_incomingclient_info, \
    ajax_task_add, get_incomingtask_info, ajax_task_update, ajax_client_add

__author__ = 'alexy'

app_name = 'incoming'

urlpatterns = [
    re_path(r'^$', login_required(IncomingClientListView.as_view()), name='list'),
    re_path(r'^add/$', incomingclient_add, name='add'),
    re_path(r'^(?P<pk>\d+)/$', incomingclient_update, name='update'),
    re_path(r'^(?P<pk>\d+)/manager/history/$', incomingclientcontact_history, name='history'),
    re_path(r'^(?P<pk>\d+)/contact/$', incomingclientcontact_list, name='contact-list'),
    re_path(r'^(?P<pk>\d+)/contact/add/$', incomingclientcontact_add, name='contact-add'),
    re_path(r'^contact/(?P<pk>\d+)/$', incomingclientcontact_update, name='contact-update'),
    re_path(r'^task/$', incomingtask_list, name='task-list'),
    # re_path(r'^task/$', IncomingTaskListView.as_view(), name='task-list'),
    re_path(r'^task/add/$', incomingtask_add, name='task-add'),
    re_path(r'^task/ajax-add/$', ajax_task_add, name='ajax-task-add'),
    re_path(r'^ajax-client-add/$', ajax_client_add, name='ajax-client-add'),
    re_path(r'^task/ajax-update/$', ajax_task_update, name='ajax-task-update'),
    re_path(r'^task/(?P<pk>\d+)/$', incomingtask_update, name='task-update'),
    re_path(r'^reassign-manager/$', reassign_manager, name='reassign-manager'),
    re_path(r'^get_available_manager_list/$', get_available_manager_list, name='get_available_manager_list'),
    re_path(r'^get_contact_list/$', get_contact_list, name='get_contact_list'),
    re_path(r'^get_incomingclient_info/$', get_incomingclient_info, name='get_incomingclient_info'),
    re_path(r'^get_incomingtask_info/$', get_incomingtask_info, name='get_incomingtask_info'),

    re_path(r'^import/$', client_list_import, name='client_list_import'),

]
