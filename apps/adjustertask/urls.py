# coding=utf-8
from django.conf.urls import patterns, url
from apps.adjustertask.ajax import adjuster_task_client, adjuster_get_area_streets, ajax_order_adjuster_list
from .views import TaskArchiveListView

__author__ = 'alexy'

urlpatterns = patterns(
    'apps.adjustertask.views',
    url(r'^$', 'adjustertask_list', name='list'),
    url(r'^archive/$', TaskArchiveListView.as_view(), name='archive'),
    url(r'^client/add/$', 'adjustertask_client', name='client-add'),
    url(r'^area/add/$', 'adjustertask_area', name='area-add'),
    url(r'^repair/add/$', 'adjustertask_repair', name='repair-add'),
    url(r'^(?P<pk>\d+)/$', 'adjuster_task_update', name='update'),

    url(r'^task_client_ajax/$', adjuster_task_client, name='client-ajax'),
    url(r'^task_area_ajax/$', adjuster_get_area_streets, name='area-ajax'),
    # получить список монтажников и заказов по id клиента
    url(r'^ajax_order_adjuster_list/$', ajax_order_adjuster_list, name='ajax-order-adjuster-list'),
)
