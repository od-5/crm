# coding=utf-8
from django.conf.urls import patterns, url
from django.contrib.admin.views.decorators import staff_member_required
from .views import SurfaceListView, SurfaceCreateView, SurfaceUpdateView, SurfacePhotoDeleteView
from .ajax import surface_map

__author__ = 'alexy'

urlpatterns = patterns(
    'apps.surface.views',
    url(r'^$', SurfaceListView.as_view(), name='list'),
    url(r'^add/$', SurfaceCreateView.as_view(), name='add'),
    url(r'^photo/$', 'surface_photo_list', name='photo-list'),
    url(r'^(?P<pk>\d+)/$', SurfaceUpdateView.as_view(), name='update'),

    url(r'^(?P<pk>\d+)/porch/$', 'surface_porch', name='porch'),
    url(r'^porch/(?P<pk>\d+)/$', 'surface_porch_update', name='porch-update'),

    url(r'^photo/add/$', 'surface_photo_add', name='photo-add'),
    url(r'^photo/(?P<pk>\d+)/$', 'surface_photo_update', name='photo-update'),
    url(r'^photo/delete/(?P<pk>\d+)/$', SurfacePhotoDeleteView.as_view(), name='photo-delete'),

    url(r'^surface-map/$', surface_map, name='surface-map'),
)
