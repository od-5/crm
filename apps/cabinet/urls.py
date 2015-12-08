# coding=utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.views import logout
from django.views.generic import ListView, UpdateView, CreateView
from django.contrib.admin.views.decorators import staff_member_required
from apps.cabinet.forms import UserChangeForm, UserAddForm
from apps.cabinet.views import UserUpdateView
from core.models import User

__author__ = 'alexy'

urlpatterns = patterns(
    'apps.cabinet.views',
    url(r'^$', 'cabinet_view', name='cabinet'),
    url(r'^user/$', staff_member_required(ListView.as_view(
        model=User,
        template_name='cabinet/user_list.html')),
        name='user-list'),
    url(r'^user/(?P<pk>\d+)/$', staff_member_required(UpdateView.as_view(
        model=User,
        form_class=UserChangeForm,
        template_name='cabinet/user_change.html',
        success_url='/cabinet/user/')),
        name='user-change'),
    url(r'^user/add/$', staff_member_required(CreateView.as_view(
        model=User,
        form_class=UserAddForm,
        template_name='cabinet/user_add.html',
        success_url='/cabinet/user/')),
        name='user-add'),
    url(r'^profile/$', UserUpdateView.as_view(), name='profile'),
    url(r'^password_change/$', 'password_change', name='password_change'),
    url(r'^login/$', 'cabinet_login', name='login'),
    url(r'^logout/$', logout, name='logout'),

)
