# coding=utf-8
from django.conf.urls import patterns, url
from django.views.generic import ListView, CreateView, UpdateView
from .models import Client
from .views import ClientListView, ClientCreateView

__author__ = 'alexy'

urlpatterns = patterns(
    'apps.client.views',
    url(r'^$', ClientListView.as_view(model=Client), name='list'),
    url(r'^add/$', 'client_add', name='add'),
    url(r'^(?P<pk>\d+)/$', UpdateView.as_view(model=Client, template_name='client/user_form.html'), name='change'),
)
