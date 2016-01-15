# coding=utf-8
from django.conf.urls import patterns, url
from ajax import client_remove
from .models import Client
from .views import ClientListView

__author__ = 'alexy'

urlpatterns = patterns(
    'apps.client.views',
    url(r'^$', ClientListView.as_view(model=Client), name='list'),
    url(r'^add/$', 'client_add', name='add'),
    url(r'^(?P<pk>\d+)/$', 'client_update', name='change'),
    url(r'^remove/$', client_remove, name='remove'),

    url(r'^(?P<pk>\d+)/maket/$', 'client_maket', name='maket'),
    url(r'^maket/add/$', 'client_maket_add', name='maket-add'),
    url(r'^maket/(?P<pk>\d+)/$', 'client_maket_update', name='maket-update'),

    url(r'^(?P<pk>\d+)/order/$', 'client_order', name='order'),
    url(r'^order/(?P<pk>\d+)/$', 'client_order_update', name='order-update'),

    url(r'^(?P<pk>\d+)/journal/$', 'client_journal', name='journal'),
    url(r'^add-surface/$', 'add_client_surface', name='add-client-surface'),


    url(r'^export/(?P<pk>\d+)/$', 'client_excel_export', name='excel_export'),
    # TODO: переделать удаление поверхности из заказа клиента
    url(r'^surface-remove/', 'remove_client_surface', name='surface-remove'),
)
