# coding=utf-8
from django.urls import include, path, re_path
from django.contrib.auth.decorators import login_required
from .ajax import get_client_order_list, get_client_order_address_list, payment_add
from .models import Client
from .views import *

__author__ = 'alexy'

app_name = 'client'

urlpatterns = [
    re_path(r'^$', login_required(ClientListView.as_view(model=Client)), name='list'),
    re_path(r'^add/$', client_add, name='add'),
    re_path(r'^(?P<pk>\d+)/$', client_update, name='change'),

    re_path(r'^(?P<pk>\d+)/maket/$', client_maket, name='maket'),
    re_path(r'^maket/add/$', client_maket_add, name='maket-add'),
    re_path(r'^maket/(?P<pk>\d+)/$', client_maket_update, name='maket-update'),

    re_path(r'^(?P<pk>\d+)/order/$', client_order, name='order'),
    re_path(r'^order/(?P<pk>\d+)/$', client_order_update, name='order-update'),
    re_path(r'^order/remove/$', ClientOrderSurfaceRemoveView.as_view(), name='order-remove'),
    re_path(r'^order/(?P<pk>\d+)/export/$', client_order_export, name='order-export'),

    re_path(r'^(?P<pk>\d+)/journal/$', client_journal, name='journal'),
    re_path(r'^journal/(?P<pk>\d+)/export/$', client_journal_export, name='journal-export'),
    re_path(r'^add-surface/$', add_client_surface, name='add-client-surface'),

    re_path(r'^get_order_list/$', get_client_order_list, name='get_order_list'),
    re_path(r'^get_order_address_list/$', get_client_order_address_list, name='get_order_address_list'),


    re_path(r'^export/(?P<pk>\d+)/$', client_excel_export, name='excel_export'),
    re_path(r'archive/$', get_files, name='download-archive'),
    re_path(r'(?P<pk>\d+)/payment/$', clientjournalpayment_list, name='payment-list'),
    re_path(r'payment/add/$', payment_add, name='payment-add'),

    path('<int:client_id>/surfaces/', login_required(ClientSurfacesView.as_view()), name='surfaces'),
    path(
        '<int:client_id>/surfaces/bind/$',
        login_required(ClientSurfaceBindView.as_view()),
        name='surface-bind'
    ),
    path('<int:client_id>/surfaces/remove/', ClientSurfaceBindRemoveView.as_view(), name='surface-bind-remove'),
]
