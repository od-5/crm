# coding=utf-8
from django.conf.urls import patterns, url
from .views import AdjusterListView
from .ajax import adjuster_map

__author__ = 'alexy'

urlpatterns = patterns(
    'apps.adjuster.views',
    url(r'^$', AdjusterListView.as_view(), name='list'),
    url(r'^add/$', 'adjuster_add', name='add'),
    url(r'^(?P<pk>\d+)/$', 'adjuster_update', name='change'),
    url(r'^(?P<pk>\d+)/task/$', 'adjuster_task', name='task'),
    url(r'^(?P<pk>\d+)/payment/$', 'adjuster_payment', name='payment'),
    url(r'^adjuster-map/$', adjuster_map, name='adjuster-map'),
)
