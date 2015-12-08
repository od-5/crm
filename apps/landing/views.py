# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render


__author__ = 'alexy'

def home_view(request):
    context = {}
    return render(request, 'landing/landing.html', context)
