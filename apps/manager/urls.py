# coding=utf-8
from django.urls import include, path, re_path
from django.contrib.auth.decorators import login_required
from apps.manager.models import Manager
from apps.manager.views import *

__author__ = 'alexy'

app_name = 'manager'

urlpatterns = [
    re_path(r'^$', login_required(ManagerListView.as_view(model=Manager)), name='list'),
    re_path(r'^add/$', manager_add, name='add'),
    re_path(r'^(?P<pk>\d+)/$', manager_update, name='update'),
    re_path(r'^report/$', manager_report, name='report'),
    re_path(r'^report/excel/$', manager_report_excel, name='report-excel'),
    re_path(r'^report/detail/(?P<pk>\d+)/$', manager_detail_report_excel, name='report-detail'),
    # re_path(r'^(?P<pk>\d+)/maket/$', 'client_maket', name='maket'),
    # re_path(r'^maket/add/$', 'client_maket_add', name='maket-add'),
    # re_path(r'^maket/(?P<pk>\d+)/$', 'client_maket_update', name='maket-update'),
    #
    # re_path(r'^(?P<pk>\d+)/order/$', 'client_order', name='order'),
    # re_path(r'^order/(?P<pk>\d+)/$', 'client_order_update', name='order-update'),
    # re_path(r'^order/(?P<pk>\d+)/export/$', 'client_order_export', name='order-export'),
    #
    # re_path(r'^(?P<pk>\d+)/journal/$', 'client_journal', name='journal'),
    # re_path(r'^journal/(?P<pk>\d+)/export/$', 'client_journal_export', name='journal-export'),
    # re_path(r'^add-surface/$', 'add_client_surface', name='add-client-surface'),
    #
    # re_path(r'^get_order_list/$', get_client_order_list, name='get_order_list'),
    # re_path(r'^get_order_address_list/$', get_client_order_address_list, name='get_order_address_list'),
    # re_path(r'^export/(?P<pk>\d+)/$', 'client_excel_export', name='excel_export'),
]
