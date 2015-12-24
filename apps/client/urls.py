# coding=utf-8
from django.conf.urls import patterns, url
from django.views.generic import DeleteView

from .models import Client, ClientSurface
from .views import ClientListView

__author__ = 'alexy'

urlpatterns = patterns(
    'apps.client.views',
    url(r'^$', ClientListView.as_view(model=Client), name='list'),
    url(r'^add/$', 'client_add', name='add'),
    url(r'^add-surface/$', 'add_client_surface', name='add-client-surface'),
    url(r'^add-maket/$', 'add_client_maket', name='add-client-maket'),
    url(r'^(?P<pk>\d+)/$', 'client_update', name='change'),
    url(r'^export/(?P<pk>\d+)/$', 'client_excel_export', name='excel_export'),
    # url(r'^surface-remove/(?P<pk>\d+)', DeleteView.as_view(model=ClientSurface, success_url="/client/"), name='surface-remove'),
    url(r'^surface-remove/', 'remove_client_surface', name='surface-remove'),
)
