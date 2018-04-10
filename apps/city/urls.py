# coding=utf-8
from django.conf.urls import patterns, url
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from apps.city.ajax import surface_ajax, get_free_area_surface, get_city_area, get_city_adjusters, \
    get_area_surface_list, simple_get_area_streets, get_area_surface_list_with_damage, get_photo_map, \
    get_simple_city_map
from .views import CityCreateView, CityListView, CityUpdateView, AreaAddView, AreaUpdateView, StreetAddView, \
    StreetUpdateView

__author__ = 'alexy'

urlpatterns = patterns(
    'apps.city.views',
    url(r'^$', login_required(CityListView.as_view()), name='list'),
    url(r'^report/$', 'city_report', name='report'),
    url(r'^add/$', staff_member_required(CityCreateView.as_view()), name='add'),
    url(r'^(?P<pk>\d+)/$', login_required(CityUpdateView.as_view()), name='update'),

    url(r'^(?P<pk>\d+)/area/$', login_required(AreaAddView.as_view()), name='area'),
    url(r'^area/(?P<pk>\d+)/$', login_required(AreaUpdateView.as_view()), name='area-update'),

    url(r'^(?P<pk>\d+)/street/$', login_required(StreetAddView.as_view()), name='street'),
    url(r'^street/(?P<pk>\d+)/$', login_required(StreetUpdateView.as_view()), name='street-update'),

    # url(r'^$', CityListView.as_view(model=City), name='management-company'),
    url(r'^management_company/$', 'management_company_list', name='management-company'),
    url(r'^management_company/add/$', 'management_company_add', name='management-company-add'),
    url(r'^management_company/(?P<pk>\d+)/$', 'management_company_update', name='management-company-update'),

    url(r'^surface-ajax/$', surface_ajax, name='surface-ajax'),

    url(r'^get_city_adjusters/$', get_city_adjusters, name='get_adjuster_list'),
    url(r'^get_city_area/$', get_city_area, name='get_area_list'),
    url(r'^simple_get_area_streets/$', simple_get_area_streets, name='simple_get_area_streets'),
    url(r'^get_free_area_surface/$', get_free_area_surface, name='get_free_area_surface'),
    url(r'^get_area_surface_list/$', get_area_surface_list, name='get_area_surface_list'),
    url(r'^get_area_surface_list_with_damage/$', get_area_surface_list_with_damage,
        name='get_area_surface_list_with_damage'),

    url(r'^get_photo_map/$', get_photo_map, name='get_photo_map'),

    url(r'^simple_city_map/$', get_simple_city_map, name='simple-map'),
)
