# coding=utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from .views import JournalListView, ClientJournalPaymentListView

__author__ = 'alexy'

urlpatterns = patterns(
    'apps.moderator.views',
    url(r'^$', login_required(JournalListView.as_view()), name='list'),
    url(r'^payment/$', login_required(ClientJournalPaymentListView.as_view()), name='payment-list'),
)
