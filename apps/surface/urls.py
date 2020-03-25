# coding=utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from apps.surface.data_import import address_list_import
from .views import SurfaceListView, SurfaceCreateView, SurfaceUpdateView, SurfacePhotoDeleteView, SurfacePhotoListView, \
    PorchView, SurfaceDocView, SurfaceDocViewWithFile, SurfacePhotoZipView
from .ajax import surface_map, ajax_photo_rotate

__author__ = 'alexy'

urlpatterns = patterns(
    'apps.surface.views',
    url(r'^$', login_required(SurfaceListView.as_view()), name='list'),
    url(r'^add/$', login_required(SurfaceCreateView.as_view()), name='add'),
    url(r'^photo/$', login_required(SurfacePhotoListView.as_view()), name='photo-list'),
    url(r'^photo/zip/$', login_required(SurfacePhotoZipView.as_view()), name='photo-zip-list'),
    url(r'^(?P<pk>\d+)/$', login_required(SurfaceUpdateView.as_view()), name='update'),

    url(r'^(?P<pk>\d+)/porch/$', login_required(PorchView.as_view()), name='porch'),
    url(r'^porch/(?P<pk>\d+)/$', 'surface_porch_update', name='porch-update'),

    url(r'^photo/add/$', 'surface_photo_add', name='photo-add'),
    url(r'^photo/(?P<pk>\d+)/$', 'surface_photo_update', name='photo-update'),
    url(r'^photo/delete/(?P<pk>\d+)/$', login_required(SurfacePhotoDeleteView.as_view()), name='photo-delete'),

    url(r'^surface-map/$', surface_map, name='surface-map'),
    url(r'^export/$', 'surface_export', name='export'),
    url(r'^import/$', address_list_import, name='import'),
    url(r'^export/docx/$', SurfaceDocView.as_view(), name='export-docx'),
    url(r'^export/docx/fromfile/$', SurfaceDocViewWithFile.as_view(), name='export-docx-from-file'),
    url(r'^update_company/$', 'update_company', name='update_company'),
    url(r'^photo-rotate/$', ajax_photo_rotate, name='photo-rotate'),
)
