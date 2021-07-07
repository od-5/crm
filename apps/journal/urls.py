# coding=utf-8
from django.urls import include, path, re_path
from django.contrib.auth.decorators import login_required
from .views import JournalListView, ClientJournalPaymentListView

__author__ = 'alexy'

app_name = 'journal'

urlpatterns = [
    re_path(r'^$', login_required(JournalListView.as_view()), name='list'),
    re_path(r'^payment/$', login_required(ClientJournalPaymentListView.as_view()), name='payment-list'),
]
