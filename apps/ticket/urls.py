# coding=utf-8
from django.urls import include, path, re_path
from .views import TicketListView, TicketUpdateView, TicketView

__author__ = 'alexy'

app_name = 'ticket'

urlpatterns = [
    re_path(r'^$', TicketView.as_view(), name='send'),
    re_path(r'^list/$', TicketListView.as_view(), name='list'),
    re_path(r'^(?P<pk>\d+)/$', TicketUpdateView.as_view(), name='detail'),
]
