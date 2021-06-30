# coding=utf-8
from django.urls import include, path, re_path
from django.contrib.auth.decorators import login_required
from .views import *
from .ajax import adjuster_map

__author__ = 'alexy'

app_name = 'adjuster'

urlpatterns = [
    re_path(r'^$', login_required(AdjusterListView.as_view()), name='list'),
    re_path(r'^add/$', adjuster_add, name='add'),
    re_path(r'^(?P<pk>\d+)/$', adjuster_update, name='change'),
    re_path(r'^(?P<pk>\d+)/task/$', adjuster_task, name='task'),
    re_path(r'^(?P<pk>\d+)/payment/$', adjuster_payment, name='payment'),
    re_path(r'^report/$', adjuster_report, name='report'),
    re_path(r'^report/excel/$', adjuster_report_excel, name='report-excel'),
    re_path(r'^report/detail/(?P<pk>\d+)/$', adjuster_detail_report_excel, name='report-detail'),
    re_path(r'^adjuster-map/$', adjuster_map, name='adjuster-map'),
]
