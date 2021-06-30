# coding=utf-8
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path, re_path


urlpatterns = [
    re_path(r'^api_v1/', include('api.urls', namespace='api')),
    re_path(r'^sign/', include('apps.sign.urls', namespace='sign'),),
    re_path(r'^cabinet/', include('apps.cabinet.urls', namespace='cabinet'),),
    re_path(r'^administrator/', include('apps.administrator.urls', namespace='administrator'),),
    re_path(r'^superviser/', include('apps.superviser.urls', namespace='superviser'),),
    re_path(r'^moderator/', include('apps.moderator.urls', namespace='moderator'),),
    re_path(r'^city/', include('apps.city.urls', namespace='city'),),
    re_path(r'^client/', include('apps.client.urls', namespace='client'),),
    re_path(r'^adjuster/', include('apps.adjuster.urls', namespace='adjuster'),),
    re_path(r'^work/', include('apps.adjuster_cabinet.urls', namespace='work'),),
    re_path(r'^task/', include('apps.adjustertask.urls', namespace='adjustertask'),),
    re_path(r'^surface/', include('apps.surface.urls', namespace='surface'),),
    re_path(r'^ticket/', include('apps.ticket.urls', namespace='ticket'),),
    re_path(r'^journal/', include('apps.journal.urls', namespace='journal'),),
    re_path(r'^manager/', include('apps.manager.urls', namespace='manager'),),
    re_path(r'^incoming/', include('apps.incoming.urls', namespace='incoming'),),
    re_path(r'', include('core.urls')),
    re_path(r'', include('apps.landing.urls')),

    re_path(r'^admin/', admin.site.urls),
    re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += [
        re_path(r'^__debug__/', include(debug_toolbar.urls)),
    ]
