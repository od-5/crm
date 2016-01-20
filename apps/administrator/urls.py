# coding=utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.views import logout
from django.contrib.admin.views.decorators import staff_member_required
from .ajax import administrator_remove
from apps.administrator.views import AdministratorListView

__author__ = 'alexy'

urlpatterns = patterns(
    'apps.administrator.views',
    url(r'^$', AdministratorListView.as_view(), name='list'),
    url(r'^add/$', 'administrator_add', name='add'),
    url(r'^remove/$', administrator_remove, name='remove'),
    url(r'^(?P<pk>\d+)/$', 'administrator_change', name='change'),
    # url(r'^user/$', staff_member_required(ListView.as_view(
    #     model=User,
    #     template_name='cabinet/user_list.html')),
    #     name='user-list'),


    # url(r'^profile/$', UserUpdateView.as_view(), name='profile'),
    # url(r'^password_change/$', 'password_change', name='password_change'),
    # url(r'^login/$', 'cabinet_login', name='login'),
    # url(r'^logout/$', logout, name='logout'),
)
