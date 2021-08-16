# coding=utf-8
from django.urls import include, path, re_path
from django.contrib.auth import logout
from django.views.generic import ListView, UpdateView, CreateView
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from .ajax import moderator_remove, moderatorinfo_update
from apps.cabinet.forms import UserChangeForm, UserAddForm
from apps.cabinet.views import UserUpdateView
from apps.moderator.views import *
from core.models import User

__author__ = 'alexy'

app_name = 'moderator'

urlpatterns = [
    re_path(r'^$', login_required(ModeratorListView.as_view()), name='list'),
    re_path(r'^add/$', moderator_add, name='add'),
    re_path(r'^remove/$', moderator_remove, name='remove'),
    re_path(r'^info/update/$', login_required(moderatorinfo_update), name='moderatorinfo'),
    re_path(r'^(?P<pk>\d+)/$', moderator_change, name='change'),
    # re_path(r'^user/$', staff_member_required(ListView.as_view(
    #     model=User,
    #     template_name='cabinet/user_list.html')),
    #     name='user-list'),


    # re_path(r'^profile/$', UserUpdateView.as_view(), name='profile'),
    # re_path(r'^password_change/$', 'password_change', name='password_change'),
    # re_path(r'^login/$', 'cabinet_login', name='login'),
    # re_path(r'^logout/$', logout, name='logout'),
]
