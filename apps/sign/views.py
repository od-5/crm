# coding=utf-8
from annoying.decorators import ajax_request
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import UpdateView
from apps.adjuster.models import Adjuster
from apps.cabinet.forms import UserProfileForm
from apps.city.models import City
from apps.client.models import Client
from core.models import User

__author__ = 'alexy'


def sign_in(request, usertype=None):
    context = {}
    error = None
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('cabinet:cabinet'))
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            try:
                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return HttpResponseRedirect(reverse('cabinet:cabinet'))
                    else:
                        error = u'Пользователь заблокирован'
                else:
                    error = u'Вы ввели неверный e-mail или пароль'
            except:
                if usertype == 2:
                    error = u'Модератора с таким e-mail не зарегистрировано в системе. Проверьте правильность ввода даных.'
                elif usertype == 3:
                    error = u'Клиента с таким e-mail не зарегистрировано в системе. Проверьте правильность ввода даных.'
                elif usertype == 4:
                    error = u'Монтажника с таким e-mail не зарегистрировано в системе. Проверьте правильность ввода даных.'
                elif usertype == 5:
                    error = u'Менеджера с таким e-mail не зарегистрировано в системе. Проверьте правильность ввода даных.'
            context.update({
                'error': error
            })
        return render(request, 'sign/login.html', context)
