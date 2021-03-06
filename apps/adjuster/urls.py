# coding=utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from .views import AdjusterListView
from .ajax import adjuster_map

__author__ = 'alexy'

urlpatterns = patterns(
    'apps.adjuster.views',
    url(r'^$', login_required(AdjusterListView.as_view()), name='list'),
    url(r'^add/$', 'adjuster_add', name='add'),
    url(r'^(?P<pk>\d+)/$', 'adjuster_update', name='change'),
    url(r'^(?P<pk>\d+)/task/$', 'adjuster_task', name='task'),
    url(r'^(?P<pk>\d+)/payment/$', 'adjuster_payment', name='payment'),
    url(r'^report/$', 'adjuster_report', name='report'),
    url(r'^report/excel/$', 'adjuster_report_excel', name='report-excel'),
    url(r'^report/detail/(?P<pk>\d+)/$', 'adjuster_detail_report_excel', name='report-detail'),
    url(r'^adjuster-map/$', adjuster_map, name='adjuster-map'),
)
