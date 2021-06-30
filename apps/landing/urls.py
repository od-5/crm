# coding=utf-8
from django.urls import include, path, re_path
from django.views.generic import TemplateView

from .views import LandingView, block_list, blockeffective_list, blockeffective_add, blockeffective_update, \
    blockreview_list, blockreview_add, blockreview_update, blockexample_list, blockexample_add, blockexample_update, \
    SiteSetupList, SetupCreateView, SetupUpdateView, OkView, NoOkView

__author__ = 'alexy'


urlpatterns = [
    re_path(r'^$', LandingView.as_view(), name='home'),
    re_path(r'^ok/$', OkView.as_view(), name='ok'),
    re_path(r'^no_ok/$', NoOkView.as_view(), name='no-ok'),
    re_path(r'^confidentiality/$', TemplateView.as_view(template_name='landing/confidentiality.html'),
        name='confidentiality'),
    # настроки лэндинга
    re_path(r'^setup/$', SiteSetupList.as_view(), name='setup-list'),
    re_path(r'^setup/add/$', SetupCreateView.as_view(), name='setup-add'),
    re_path(r'^setup/(?P<pk>\d+)/$', SetupUpdateView.as_view(), name='setup-update'),
    # Список блоков для редактирования
    re_path(r'^block/$', block_list, name='block-list'),
    # блок "почему реклама на подъездах так эффективна"
    re_path(r'^block/effective/$', blockeffective_list, name='blockeffective-list'),
    re_path(r'^block/effective/add/$', blockeffective_add, name='blockeffective-add'),
    re_path(r'^block/effective/(?P<pk>\d+)/$', blockeffective_update, name='blockeffective-update'),
    # блок "Отзывы об эффективности нашей рекламы"
    re_path(r'^block/review/$', blockreview_list, name='blockreview-list'),
    re_path(r'^block/review/add/$', blockreview_add, name='blockreview-add'),
    re_path(r'^block/review/(?P<pk>\d+)/$', blockreview_update, name='blockreview-update'),
    # блок "Примеры размещений"
    re_path(r'^block/example/$', blockexample_list, name='blockexample-list'),
    re_path(r'^block/example/add/$', blockexample_add, name='blockexample-add'),
    re_path(r'^block/example/(?P<pk>\d+)/$', blockexample_update, name='blockexample-update'),
]
