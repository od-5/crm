# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.generic import ListView, UpdateView, CreateView
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import include, path, re_path

from apps.cabinet.forms import UserChangeForm, UserAddForm
from apps.cabinet.views import *
from core.models import User

__author__ = 'alexy'

app_name = 'cabinet'

urlpatterns = [
    re_path(r'^$', cabinet_view, name='cabinet'),
    re_path(r'^user/$', staff_member_required(ListView.as_view(
        model=User,
        template_name='cabinet/user_list.html')),
        name='user-list'),
    re_path(r'^user/(?P<pk>\d+)/$', staff_member_required(UpdateView.as_view(
        model=User,
        form_class=UserChangeForm,
        template_name='cabinet/user_change.html',
        success_url='/cabinet/user/')),
        name='user-change'),
    re_path(r'^user/add/$', staff_member_required(CreateView.as_view(
        model=User,
        form_class=UserAddForm,
        template_name='cabinet/user_add.html',
        success_url='/cabinet/user/')),
        name='user-add'),
    re_path(r'^profile/$', login_required(UserUpdateView.as_view()), name='profile'),
    re_path(r'^password_change/$', password_change, name='password_change'),
    re_path(r'^login/$', cabinet_login, name='login'),
    re_path(r'^logout/$', logout, name='logout'),
]
