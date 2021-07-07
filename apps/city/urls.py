# coding=utf-8
from django.urls import include, path, re_path
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from apps.city.ajax import surface_ajax, get_free_area_surface, get_city_area, get_city_adjusters, \
    get_area_surface_list, simple_get_area_streets, get_area_surface_list_with_damage, get_photo_map, \
    get_simple_city_map
from .views import *

__author__ = 'alexy'

app_name = 'city'
urlpatterns = [
    re_path(r'^$', login_required(CityListView.as_view()), name='list'),
    re_path(r'^report/$', city_report, name='report'),
    re_path(r'^add/$', staff_member_required(CityCreateView.as_view()), name='add'),
    re_path(r'^(?P<pk>\d+)/$', login_required(CityUpdateView.as_view()), name='update'),

    re_path(r'^(?P<pk>\d+)/area/$', login_required(AreaAddView.as_view()), name='area'),
    re_path(r'^area/(?P<pk>\d+)/$', login_required(AreaUpdateView.as_view()), name='area-update'),

    re_path(r'^(?P<pk>\d+)/street/$', login_required(StreetAddView.as_view()), name='street'),
    re_path(r'^street/(?P<pk>\d+)/$', login_required(StreetUpdateView.as_view()), name='street-update'),

    # re_path(r'^$', CityListView.as_view(model=City), name='management-company'),
    re_path(r'^management_company/$', management_company_list, name='management-company'),
    re_path(r'^management_company/add/$', management_company_add, name='management-company-add'),
    re_path(r'^management_company/(?P<pk>\d+)/$', management_company_update, name='management-company-update'),

    re_path(r'^surface-ajax/$', surface_ajax, name='surface-ajax'),

    re_path(r'^get_city_adjusters/$', get_city_adjusters, name='get_adjuster_list'),
    re_path(r'^get_city_area/$', get_city_area, name='get_area_list'),
    re_path(r'^simple_get_area_streets/$', simple_get_area_streets, name='simple_get_area_streets'),
    re_path(r'^get_free_area_surface/$', get_free_area_surface, name='get_free_area_surface'),
    re_path(r'^get_area_surface_list/$', get_area_surface_list, name='get_area_surface_list'),
    re_path(r'^get_area_surface_list_with_damage/$', get_area_surface_list_with_damage,
        name='get_area_surface_list_with_damage'),

    re_path(r'^get_photo_map/$', get_photo_map, name='get_photo_map'),

    re_path(r'^simple_city_map/$', get_simple_city_map, name='simple-map'),
]
