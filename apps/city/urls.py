# coding=utf-8
from django.conf.urls import patterns, url
from django.contrib.admin.views.decorators import staff_member_required
from apps.city.ajax import surface_ajax, get_area_streets, get_city_area
from .models import City
from .views import CityCreateView, CityListView

__author__ = 'alexy'

urlpatterns = patterns(
    'apps.city.views',
    url(r'^$', CityListView.as_view(model=City), name='list'),
    url(r'^add/$', staff_member_required(CityCreateView.as_view()), name='add'),
    url(r'^(?P<pk>\d+)/$', 'city_update', name='update'),

    url(r'^(?P<pk>\d+)/area/$', 'city_area', name='area'),
    url(r'^area/(?P<pk>\d+)/$', 'city_area_update', name='area-update'),

    url(r'^(?P<pk>\d+)/street/$', 'city_street', name='street'),
    url(r'^street/(?P<pk>\d+)/$', 'city_street_update', name='street-update'),



    url(r'^surface-ajax/$', surface_ajax, name='surface-ajax'),
    url(r'^get_area_streets/$', get_area_streets, name='get_area_streets'),
    url(r'^get_city_area/$', get_city_area, name='get_city_area'),
)
