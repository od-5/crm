# coding=utf-8
from django.conf.urls import patterns, url
from .views import IncomingClientListView, IncomingTaskListView
from .ajax import reassign_manager, get_available_manager_list, get_contact_list

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
    url(r'^task/(?P<pk>\d+)/$', 'incomingtask_update', name='task-update'),
    url(r'^reassign-manager/$', reassign_manager, name='reassign-manager'),
    url(r'^get_available_manager_list/$', get_available_manager_list, name='get_available_manager_list'),
    url(r'^get_contact_list/$', get_contact_list, name='get_contact_list'),
)

