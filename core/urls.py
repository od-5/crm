# coding=utf-8
from django.conf.urls import patterns, url
from core.ajax import ymap, ymap_surface, ajax_remove_item

__author__ = 'alexy'


urlpatterns = patterns(
    'core.views',
    url(r'^robots\.txt', 'get_robots_txt', name='robots'),
    url(r'^configure/$', 'site_config_view', name='site_configure'),

    url(r'^block/$', 'block_list', name='block'),
    url(r'^block/effective/add/$', 'block_effective_add_view', name='block_effective-add'),
    url(r'^block/effective/(?P<pk>\d+)/$', 'block_effective_update_view', name='block_effective-update'),
    url(r'^block/effective/$', 'block_effective_view', name='block_effective'),

    url(r'^block/example/add/$', 'block_example_add_view', name='block_example-add'),
    url(r'^block/example/(?P<pk>\d+)/$', 'block_example_update_view', name='block_example-update'),
    url(r'^block/example/$', 'block_example_view', name='block_example'),

    url(r'^block/review/add/$', 'block_review_add_view', name='block_review-add'),
    url(r'^block/review/(?P<pk>\d+)/$', 'block_review_update_view', name='block_review-update'),
    url(r'^block/review/$', 'block_review_view', name='block_review'),
    url(r'^city-map/$', ymap, name='map'),
    url(r'^surface-map/$', ymap_surface, name='map-surface'),
    url(r'^ajax_remove/$', ajax_remove_item, name='ajax-remove'),

    # url(r'^cabinet/login/$', 'cabinet_login', name='login'),
    # url(r'^cabinet/logout/$', logout, name='logout'),

)
