# coding=utf-8
from django.urls import include, path, re_path
from core.ajax import ymap, ymap_surface, ajax_remove_item
from core.views import get_robots_txt

__author__ = 'alexy'


urlpatterns = [
    re_path(r'^robots\.txt', get_robots_txt, name='robots'),

    # re_path(r'^block/example/add/$', 'block_example_add_view', name='block_example-add'),
    # re_path(r'^block/example/(?P<pk>\d+)/$', 'block_example_update_view', name='block_example-update'),
    # re_path(r'^block/example/$', 'block_example_view', name='block_example'),


    re_path(r'^city-map/$', ymap, name='map'),
    re_path(r'^surface-map/$', ymap_surface, name='map-surface'),
    re_path(r'^ajax_remove/$', ajax_remove_item, name='ajax-remove'),

    # re_path(r'^cabinet/login/$', 'cabinet_login', name='login'),
    # re_path(r'^cabinet/logout/$', logout, name='logout'),

]
