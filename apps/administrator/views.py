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
from core.forms import UserAddForm, UserUpdateForm
from core.models import User

__author__ = 'alexy'


def administrator_add(request):
    context = {}
    if request.method == "POST":
        form = UserAddForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.type = 1
            user.save()
            return HttpResponseRedirect(reverse('administrator:change', args=(user.id, )))
        else:
            context.update({
                'error': u'Проверьте правильность ввода полей'
            })
    else:
        form = UserAddForm()
    context.update({
        'form': form,
    })
    return render(request, 'administrator/administrator_add.html', context)


def administrator_change(request, pk):
    context = {}
    user = User.objects.get(pk=int(pk))
    success_msg = u''
    error_msg = u''
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 and password2:
            if password1 == password2:
                user.set_password(password1)
                success_msg = u'Пароль успешно изменён!'
            else:
                error_msg = u'Пароль и подтверждение пароля не совпадают!'
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            success_msg += u' Изменения успешно сохранены'
        else:
            error_msg = u'Проверьте правильность ввода полей!'
    else:
        form = UserUpdateForm(instance=user)
    context.update({
        'success': success_msg,
        'error': error_msg,
        'form': form,
        'object': user
    })
    return render(request, 'administrator/administrator_change.html', context)

