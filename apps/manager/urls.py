# coding=utf-8
from django.conf.urls import patterns, url
from apps.manager.models import Manager
from apps.manager.views import ManagerListView

__author__ = 'alexy'

urlpatterns = patterns(
    'apps.manager.views',
    url(r'^$', ManagerListView.as_view(model=Manager), name='list'),
    url(r'^add/$', 'manager_add', name='add'),
    url(r'^(?P<pk>\d+)/$', 'manager_update', name='update'),
    url(r'^report/$', 'manager_report', name='report'),
    url(r'^report/excel/$', 'manager_report_excel', name='report-excel'),
    url(r'^report/detail/(?P<pk>\d+)/$', 'manager_detail_report_excel', name='report-detail'),
    # url(r'^(?P<pk>\d+)/maket/$', 'client_maket', name='maket'),
    # url(r'^maket/add/$', 'client_maket_add', name='maket-add'),
    # url(r'^maket/(?P<pk>\d+)/$', 'client_maket_update', name='maket-update'),
    #
    # url(r'^(?P<pk>\d+)/order/$', 'client_order', name='order'),
    # url(r'^order/(?P<pk>\d+)/$', 'client_order_update', name='order-update'),
    # url(r'^order/(?P<pk>\d+)/export/$', 'client_order_export', name='order-export'),
    #
    # url(r'^(?P<pk>\d+)/journal/$', 'client_journal', name='journal'),
    # url(r'^journal/(?P<pk>\d+)/export/$', 'client_journal_export', name='journal-export'),
    # url(r'^add-surface/$', 'add_client_surface', name='add-client-surface'),
    #
    # url(r'^get_order_list/$', get_client_order_list, name='get_order_list'),
    # url(r'^get_order_address_list/$', get_client_order_address_list, name='get_order_address_list'),
    # url(r'^export/(?P<pk>\d+)/$', 'client_excel_export', name='excel_export'),
)
