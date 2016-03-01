# coding=utf-8
from django.conf.urls import patterns, url

__author__ = 'alexy'

urlpatterns = patterns(
    'apps.sign.views',
    # url(r'^moderator/$', 'moderator_sign', name='moderator'),
    # url(r'^manager/$', 'manager_sign', name='manager'),
    # url(r'^client/$', 'client_sign', name='client'),
    # url(r'^adjuster/$', 'adjuster_sign', name='adjuster'),
    url(r'^moderator/$', 'sign_in', {'usertype': 2}, name='moderator'),
    url(r'^client/$', 'sign_in', {'usertype': 3},  name='client'),
    url(r'^adjuster/$', 'sign_in', {'usertype': 4}, name='adjuster'),
    url(r'^manager/$', 'sign_in', {'usertype': 5},  name='manager'),
)
