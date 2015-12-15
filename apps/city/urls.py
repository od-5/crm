# coding=utf-8
from django.conf.urls import patterns, url
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import CreateView
from apps.city.ajax import surface_ajax
from .forms import CityAddForm
from .models import City, Surface
from .views import city_update, SurfaceListView, SurfaceCreateView, SurfaceUpdateView, CityListView

__author__ = 'alexy'

urlpatterns = patterns(
    'apps.city.views',
    url(r'^$', CityListView.as_view(model=City), name='list'),
    url(r'^add/$', staff_member_required(CreateView.as_view(model=City, form_class=CityAddForm)), name='add'),
    url(r'^(?P<pk>\d+)/$', city_update, name='change'),
    url(r'^porch-add/$', 'porch_update', name='porch'),
    url(r'^street-add/$', 'street_add', name='street-add'),
    url(r'^surface/$', SurfaceListView.as_view(), name='surface-list'),
    url(r'^surface-ajax/$', surface_ajax, name='surface-ajax'),
    url(r'^surface/add$', SurfaceCreateView.as_view(), name='surface-add'),
    url(r'^surface/(?P<pk>\d+)', SurfaceUpdateView.as_view(), name='surface-change'),
    # url(r'^surface/(?P<pk>\d+)', surface_update, name='surface-change'),
)
