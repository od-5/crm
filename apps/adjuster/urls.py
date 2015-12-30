# coding=utf-8
from django.conf.urls import patterns, url
from apps.adjuster.ajax import adjuster_remove
from .views import AdjusterListView

__author__ = 'alexy'

urlpatterns = patterns(
    'apps.adjuster.views',
    url(r'^$', AdjusterListView.as_view(), name='list'),
    url(r'^add/$', 'adjuster_add', name='add'),
    url(r'^(?P<pk>\d+)/$', 'adjuster_update', name='change'),
    url(r'^remove/$', adjuster_remove, name='remove'),
)
