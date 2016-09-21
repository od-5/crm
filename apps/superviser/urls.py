# coding=utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from .views import SuperviserListView

__author__ = 'alexy'

urlpatterns = patterns(
    'apps.superviser.views',
    url(r'^$', login_required(SuperviserListView.as_view()), name='list'),
    url(r'^add/$', 'superviser_add', name='add'),
    url(r'^(?P<pk>\d+)/$', 'superviser_update', name='update'),
    # url(r'^user/$', staff_member_required(ListView.as_view(
    #     model=User,
    #     template_name='cabinet/user_list.html')),
    #     name='user-list'),


    # url(r'^profile/$', UserUpdateView.as_view(), name='profile'),
    # url(r'^password_change/$', 'password_change', name='password_change'),
    # url(r'^login/$', 'cabinet_login', name='login'),
    # url(r'^logout/$', logout, name='logout'),
)
