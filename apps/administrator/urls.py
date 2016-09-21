# coding=utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from apps.administrator.views import AdministratorListView

__author__ = 'alexy'

urlpatterns = patterns(
    'apps.administrator.views',
    url(r'^$', login_required(AdministratorListView.as_view()), name='list'),
    url(r'^add/$', 'administrator_add', name='add'),
    url(r'^(?P<pk>\d+)/$', 'administrator_update', name='update'),
)
