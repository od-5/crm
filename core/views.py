# coding=utf-8
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from apps.landing.models import Setup

__author__ = 'alexy'


def get_robots_txt(request):
    """
    Функция отображения robots.txt
    """
    if request.subdomain:
        try:
            setup = Setup.objects.get(city__slug=request.subdomain)
        except:
            try:
                setup = Setup.objects.filter(city__isnull=True).first()
            except:
                setup = Setup.objects.all().first()
    else:
        try:
            setup = Setup.objects.filter(city__isnull=True).first()
        except:
            setup = Setup.objects.all().first()
    try:
        content = setup.robots_txt
    except:
        content = u'User-agent: *'
    robots_response = HttpResponse(content, content_type='text/plain')
    return robots_response
