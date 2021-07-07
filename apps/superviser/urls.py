# coding=utf-8
from django.urls import include, path, re_path
from django.contrib.auth.decorators import login_required
from .views import *

__author__ = 'alexy'

app_name = 'superviser'

urlpatterns = [
    re_path(r'^$', login_required(SuperviserListView.as_view()), name='list'),
    re_path(r'^add/$', superviser_add, name='add'),
    re_path(r'^(?P<pk>\d+)/$', superviser_update, name='update'),
    # re_path(r'^user/$', staff_member_required(ListView.as_view(
    #     model=User,
    #     template_name='cabinet/user_list.html')),
    #     name='user-list'),


    # re_path(r'^profile/$', UserUpdateView.as_view(), name='profile'),
    # re_path(r'^password_change/$', 'password_change', name='password_change'),
    # re_path(r'^login/$', 'cabinet_login', name='login'),
    # re_path(r'^logout/$', logout, name='logout'),
]
