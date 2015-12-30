# coding=utf-8
from django.conf.urls import patterns, url
from django.contrib.admin.views.decorators import staff_member_required
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, DeleteView
from apps.city.ajax import surface_ajax, get_area_streets, city_remove
from .forms import CityAddForm
from .models import City, Surface, Street
from .views import city_update, SurfaceListView, SurfaceCreateView, SurfaceUpdateView, CityListView

__author__ = 'alexy'

urlpatterns = patterns(
    'apps.city.views',
    url(r'^$', CityListView.as_view(model=City), name='list'),
    url(r'^add/$', staff_member_required(CreateView.as_view(model=City, form_class=CityAddForm)), name='add'),
    url(r'^(?P<pk>\d+)/$', city_update, name='change'),
    url(r'^remove/$', city_remove, name='remove'),
    url(r'^porch-add/$', 'porch_update', name='porch'),
    url(r'^street-add/$', 'street_add', name='street-add'),
    url(r'^surface/$', SurfaceListView.as_view(), name='surface-list'),
    url(r'^surface-ajax/$', surface_ajax, name='surface-ajax'),
    url(r'^surface/add$', SurfaceCreateView.as_view(), name='surface-add'),
    url(r'^add-surface/$', 'add_surface_client', name='add-surface-client'),
    url(r'^photo-add/$', 'surface_photo_add', name='photo-add'),
    url(r'^get_area_streets/$', get_area_streets, name='get_area_streets'),
    url(r'^surface/(?P<pk>\d+)', SurfaceUpdateView.as_view(), name='surface-change'),
    url(r'^surface-remove/(?P<pk>\d+)', DeleteView.as_view(model=Surface, success_url="/city/surface/", template_name="city/street_confirm_delete.html"), name='surface-remove'),
    url(r'^street-remove/(?P<pk>\d+)', DeleteView.as_view(model=Street, success_url="/city/"), name='street-remove'),
    # url(r'^surface/(?P<pk>\d+)', surface_update, name='surface-change'),
)
