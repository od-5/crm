# coding=utf-8
from django.conf.urls import patterns, url
from .views import TicketListView, TicketUpdateView, TicketView

__author__ = 'alexy'


urlpatterns = patterns(
    '',
    url(r'^$', TicketView.as_view(), name='send'),
    url(r'^list/$', TicketListView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', TicketUpdateView.as_view(), name='detail'),
)
