# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from apps.city.models import City
from core.models import Setup

__author__ = 'alexy'


def home_view(request):
    context = {}
    user = request.user
    city_qs = City.objects.all()
    city_count = city_qs.count()
    city_list_1 = city_qs[0:(city_count/2)]
    city_list_2 = city_qs[(city_count/2):]
    setup = Setup.objects.all().first()
    context.update({
        'setup': setup,
        'city_list': city_qs,
        'city_list_1': city_list_1,
        'city_list_2': city_list_2
    })
    return render(request, 'landing/index.html', context)
