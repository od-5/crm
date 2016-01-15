# coding=utf-8
from django.conf.urls import patterns, url
from core.ajax import ymap, ymap_surface, ajax_remove_item

__author__ = 'alexy'


urlpatterns = patterns(
    'core.views',
    url(r'^robots\.txt', 'get_robots_txt', name='robots'),
    url(r'^city-map/$', ymap, name='map'),
    url(r'^surface-map/$', ymap_surface, name='map-surface'),
    url(r'^ajax_remove/$', ajax_remove_item, name='ajax-remove'),

    # url(r'^cabinet/login/$', 'cabinet_login', name='login'),
    # url(r'^cabinet/logout/$', logout, name='logout'),

)
