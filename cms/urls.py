# coding=utf-8
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import debug_toolbar
from django.views.generic import TemplateView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', TemplateView.as_view(template_name='landing/landing.html'), name='home'),
    url(r'^$', 'apps.landing.views.home_view', name='home'),
    url(r'^cabinet/', include('apps.cabinet.urls', namespace='cabinet'),),
    url(r'^administrator/', include('apps.administrator.urls', namespace='administrator'),),
    url(r'^moderator/', include('apps.moderator.urls', namespace='moderator'),),
    url(r'^city/', include('apps.city.urls', namespace='city'),),
    url(r'^client/', include('apps.client.urls', namespace='client'),),
    url(r'^adjuster/', include('apps.adjuster.urls', namespace='adjuster'),),
    url(r'^ticket/', include('apps.ticket.urls', namespace='ticket'),),
    url(r'', include('core.urls')),

    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns(
        '',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
