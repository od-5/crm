# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.urls import include, path, re_path

from apps.administrator.views import *

__author__ = 'alexy'

app_name = 'administrator'

urlpatterns = [
    re_path(r'^$', login_required(AdministratorListView.as_view()), name='list'),
    re_path(r'^add/$', administrator_add, name='add'),
    re_path(r'^(?P<pk>\d+)/$', administrator_update, name='update'),
]
