# coding=utf-8
from django.urls import include, path, re_path
from django.contrib.auth.decorators import login_required
from apps.surface.data_import import address_list_import
from .views import *
from .ajax import surface_map, ajax_photo_rotate

__author__ = 'alexy'

app_name = 'surface'

urlpatterns = [
    re_path(r'^$', login_required(SurfaceListView.as_view()), name='list'),
    re_path(r'^add/$', login_required(SurfaceCreateView.as_view()), name='add'),
    re_path(r'^photo/$', login_required(SurfacePhotoListView.as_view()), name='photo-list'),
    re_path(r'^photo/zip/$', login_required(SurfacePhotoZipView.as_view()), name='photo-zip-list'),
    re_path(r'^(?P<pk>\d+)/$', login_required(SurfaceUpdateView.as_view()), name='update'),
    path('<int:pk>/orders/', login_required(SurfaceOrdersView.as_view()), name='orders'),

    re_path(r'^(?P<pk>\d+)/porch/$', login_required(PorchView.as_view()), name='porch'),
    re_path(r'^porch/(?P<pk>\d+)/$', surface_porch_update, name='porch-update'),

    re_path(r'^photo/add/$', surface_photo_add, name='photo-add'),
    re_path(r'^photo/(?P<pk>\d+)/$', surface_photo_update, name='photo-update'),
    re_path(r'^photo/delete/(?P<pk>\d+)/$', login_required(SurfacePhotoDeleteView.as_view()), name='photo-delete'),

    re_path(r'^surface-map/$', surface_map, name='surface-map'),
    re_path(r'^export/$', surface_export, name='export'),
    re_path(r'^import/$', address_list_import, name='import'),
    re_path(r'^export/docx/$', SurfaceDocView.as_view(), name='export-docx'),
    re_path(r'^export/docx/fromfile/$', SurfaceDocViewWithFile.as_view(), name='export-docx-from-file'),
    re_path(r'^update_company/$', update_company, name='update_company'),
    re_path(r'^photo-rotate/$', ajax_photo_rotate, name='photo-rotate'),
]
