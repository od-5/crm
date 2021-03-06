# coding=utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from ajax import get_client_order_list, get_client_order_address_list, payment_add
from .models import Client
from .views import ClientListView, ClientOrderSurfaceRemoveView

__author__ = 'alexy'

urlpatterns = patterns(
    'apps.client.views',
    url(r'^$', login_required(ClientListView.as_view(model=Client)), name='list'),
    url(r'^add/$', 'client_add', name='add'),
    url(r'^(?P<pk>\d+)/$', 'client_update', name='change'),

    url(r'^(?P<pk>\d+)/maket/$', 'client_maket', name='maket'),
    url(r'^maket/add/$', 'client_maket_add', name='maket-add'),
    url(r'^maket/(?P<pk>\d+)/$', 'client_maket_update', name='maket-update'),

    url(r'^(?P<pk>\d+)/order/$', 'client_order', name='order'),
    url(r'^order/(?P<pk>\d+)/$', 'client_order_update', name='order-update'),
    url(r'^order/remove/$', ClientOrderSurfaceRemoveView.as_view(), name='order-remove'),
    url(r'^order/(?P<pk>\d+)/export/$', 'client_order_export', name='order-export'),

    url(r'^(?P<pk>\d+)/journal/$', 'client_journal', name='journal'),
    url(r'^journal/(?P<pk>\d+)/export/$', 'client_journal_export', name='journal-export'),
    url(r'^add-surface/$', 'add_client_surface', name='add-client-surface'),

    url(r'^get_order_list/$', get_client_order_list, name='get_order_list'),
    url(r'^get_order_address_list/$', get_client_order_address_list, name='get_order_address_list'),


    url(r'^export/(?P<pk>\d+)/$', 'client_excel_export', name='excel_export'),
    url(r'archive/$', 'get_files', name='download-archive'),
    url(r'(?P<pk>\d+)/payment/$', 'clientjournalpayment_list', name='payment-list'),
    url(r'payment/add/$', payment_add, name='payment-add')
)
