# coding=utf-8
from django.conf.urls import patterns, url
from apps.administrator.views import AdministratorListView

__author__ = 'alexy'

urlpatterns = patterns(
    'apps.administrator.views',
    url(r'^$', AdministratorListView.as_view(), name='list'),
    url(r'^add/$', 'administrator_add', name='add'),
    url(r'^(?P<pk>\d+)/$', 'administrator_update', name='update'),
)
