# coding=utf-8
from django.conf.urls import patterns, url
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import ListView, CreateView
from .forms import CityAddForm
from .models import City
from .views import city_update

__author__ = 'alexy'

urlpatterns = patterns(
    'apps.city.views',
    url(r'^$', staff_member_required(ListView.as_view(model=City)), name='list'),
    url(r'^add/$', staff_member_required(CreateView.as_view(model=City, form_class=CityAddForm)), name='add'),
    url(r'^(?P<pk>\d+)/$', staff_member_required(city_update), name='change'),
)
