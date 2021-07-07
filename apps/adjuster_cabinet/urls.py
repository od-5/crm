# coding=utf-8
from django.urls import include, path, re_path

from .views import *

__author__ = 'alexy'

app_name = 'work'

urlpatterns = [
    re_path(r'^$', task_list, name='list'),
    re_path(r'^(?P<pk>\d+)/$', task_detail, name='detail'),
    re_path(r'^address/(?P<pk>\d+)$', address_detail, name='address-detail'),
    re_path(r'^address/porch/(?P<pk>\d+)$', porch_detail, name='porch-detail'),
    re_path(r'^address/porch/(?P<pk>\d+)/photo/$', photo_add, name='porch-photo-add'),
]
