# coding=utf-8
from django.conf.urls import patterns, url
from .views import JournalListView, ClientJournalPaymentListView

__author__ = 'alexy'

urlpatterns = patterns(
    'apps.moderator.views',
    url(r'^$', JournalListView.as_view(), name='list'),
    url(r'^payment/$', ClientJournalPaymentListView.as_view(), name='payment-list'),
)
