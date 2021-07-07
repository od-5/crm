# coding=utf-8
from django.urls import include, path, re_path

from .views import *

__author__ = 'alexy'

app_name = 'sign'

urlpatterns = [
    # re_path(r'^moderator/$', 'moderator_sign', name='moderator'),
    # re_path(r'^manager/$', 'manager_sign', name='manager'),
    # re_path(r'^client/$', 'client_sign', name='client'),
    # re_path(r'^adjuster/$', 'adjuster_sign', name='adjuster'),
    re_path(r'^moderator/$', sign_in, {'usertype': 2}, name='moderator'),
    re_path(r'^client/$', sign_in, {'usertype': 3}, name='client'),
    re_path(r'^adjuster/$', sign_in, {'usertype': 4}, name='adjuster'),
    re_path(r'^manager/$', sign_in, {'usertype': 5}, name='manager'),
]
