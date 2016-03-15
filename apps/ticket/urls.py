# coding=utf-8
from django.conf.urls import patterns, url

__author__ = 'alexy'


urlpatterns = patterns(
    'apps.ticket.ajax',
    url(r'^$', 'ticket', name='send'),
)
