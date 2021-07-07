# coding=utf-8
from django.urls import include, path, re_path
from apps.adjustertask.ajax import adjuster_task_client, adjuster_get_area_streets, ajax_order_adjuster_list
from .views import *

__author__ = 'alexy'

app_name = 'adjustertask'

urlpatterns = [
    re_path(r'^$', adjustertask_list, name='list'),
    re_path(r'^archive/$', TaskArchiveListView.as_view(), name='archive'),
    re_path(r'^client/add/$', adjustertask_client, name='client-add'),
    re_path(r'^area/add/$', adjustertask_area, name='area-add'),
    re_path(r'^repair/add/$', adjustertask_repair, name='repair-add'),
    re_path(r'^(?P<pk>\d+)/$', adjuster_task_update, name='update'),

    re_path(r'^task_client_ajax/$', adjuster_task_client, name='client-ajax'),
    re_path(r'^task_area_ajax/$', adjuster_get_area_streets, name='area-ajax'),
    # получить список монтажников и заказов по id клиента
    re_path(r'^ajax_order_adjuster_list/$', ajax_order_adjuster_list, name='ajax-order-adjuster-list'),
]
