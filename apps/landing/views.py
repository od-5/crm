# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from apps.city.models import City

__author__ = 'alexy'

def home_view(request):
    context = {}
    city_qs = City.objects.all()
    context.update({
        'city_list': city_qs
    })
    return render(request, 'landing/index.html', context)
