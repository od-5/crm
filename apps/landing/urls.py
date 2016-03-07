# coding=utf-8
from django.conf.urls import patterns, url

__author__ = 'alexy'


urlpatterns = patterns(
    'apps.landing.views',
    url(r'^$', 'home_view', name='home'),
    # настроки лэндинга
    url(r'^setup/$', 'setup_list', name='setup-list'),
    url(r'^setup/add/$', 'setup_add', name='setup-add'),
    url(r'^setup/(?P<pk>\d+)/$', 'setup_update', name='setup-update'),
    # Список блоков для редактирования
    url(r'^block/$', 'block_list', name='block-list'),
    # блок "почему реклама на подъездах так эффективна"
    url(r'^block/effective/$', 'blockeffective_list', name='blockeffective-list'),
    url(r'^block/effective/add/$', 'blockeffective_add', name='blockeffective-add'),
    url(r'^block/effective/(?P<pk>\d+)/$', 'blockeffective_update', name='blockeffective-update'),
    # блок "Отзывы об эффективности нашей рекламы"
    url(r'^block/review/$', 'blockreview_list', name='blockreview-list'),
    url(r'^block/review/add/$', 'blockreview_add', name='blockreview-add'),
    url(r'^block/review/(?P<pk>\d+)/$', 'blockreview_update', name='blockreview-update'),
    # блок "Примеры размещений"
    url(r'^block/example/$', 'blockexample_list', name='blockexample-list'),
    url(r'^block/example/add/$', 'blockexample_add', name='blockexample-add'),
    url(r'^block/example/(?P<pk>\d+)/$', 'blockexample_update', name='blockexample-update'),


)