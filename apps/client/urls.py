# coding=utf-8
from django.conf.urls import patterns, url
from .models import Client
from .views import ClientListView

__author__ = 'alexy'

urlpatterns = patterns(
    'apps.client.views',
    url(r'^$', ClientListView.as_view(model=Client), name='list'),
    url(r'^add/$', 'client_add', name='add'),
    url(r'^(?P<pk>\d+)/$', 'client_update', name='change'),
)
