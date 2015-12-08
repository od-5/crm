# coding=utf-8
from django.http import HttpResponse
from core.models import Setup

__author__ = 'alexy'


def get_robots_txt(request):
    try:
        content = Setup.objects.all()[0].robots_txt
    except:
        content = u'User-agent: *'
    robots_response = HttpResponse(content, content_type='text/plain')
    return robots_response
