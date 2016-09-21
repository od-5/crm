# coding=utf-8
from django.conf.urls import patterns, url

__author__ = 'alexy'

urlpatterns = patterns(
    'apps.adjuster_cabinet.views',
    url(r'^$', 'task_list', name='list'),
    url(r'^(?P<pk>\d+)/$', 'task_detail', name='detail'),
    url(r'^address/(?P<pk>\d+)$', 'address_detail', name='address-detail'),
    url(r'^address/porch/(?P<pk>\d+)$', 'porch_detail', name='porch-detail'),
    url(r'^address/porch/(?P<pk>\d+)/photo/$', 'photo_add', name='porch-photo-add'),
)
