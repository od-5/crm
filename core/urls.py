# coding=utf-8
from django.conf.urls import patterns, url

__author__ = 'alexy'


urlpatterns = patterns(
    'core.views',
    url(r'^robots\.txt', 'get_robots_txt', name='robots'),

    # url(r'^cabinet/login/$', 'cabinet_login', name='login'),
    # url(r'^cabinet/logout/$', logout, name='logout'),

)
