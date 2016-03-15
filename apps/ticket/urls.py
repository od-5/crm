# coding=utf-8
from django.conf.urls import patterns, url
from .ajax import ticket
from .views import TicketListView


__author__ = 'alexy'


urlpatterns = patterns(
    'apps.ticket.views',
    url(r'^$', ticket, name='send'),
    url(r'^list/$', TicketListView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', 'ticket_detail', name='detail'),
)
