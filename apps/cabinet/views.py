# coding=utf-8
from annoying.decorators import ajax_request
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.views.generic import UpdateView
from apps.adjuster.models import Adjuster
from apps.cabinet.forms import UserProfileForm
from apps.city.models import City
from apps.client.models import Client
from core.models import User

__author__ = 'alexy'


@login_required()
def cabinet_view(request):
    context = {}
    user = request.user
    if user.type == 1:
        template_name = 'cabinet/dash_admin.html'
    elif user.type == 2:
        template_name = 'cabinet/dash_moderator.html'
    elif user.type == 3:
        template_name = 'cabinet/dash_client.html'
    elif user.type == 4:
        template_name = 'cabinet/dash_adjuster.html'
    elif user.type == 5:
        template_name = 'cabinet/dash_manager.html'
    else:
        raise Http404
    return render(request, template_name, context)


def cabinet_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect(reverse('cabinet:cabinet'))
        else:
            error = u'Пользователь заблокирован'
    else:
        error = u'Вы ввели неверный e-mail или пароль'
    context = {'error': error}
    return render(request, 'cabinet/login.html', context)


class UserUpdateView(UpdateView):
    model = User
    template_name = 'cabinet/profile.html'
    form_class = UserProfileForm
    success_url = '/cabinet/profile/'

    def get_object(self, queryset=None):
        return self.request.user

@ajax_request
def password_change(request):
    user_id = request.POST.get('user_id')
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')
    try:
        user = User.objects.get(pk=int(user_id))
        if password1 and password2 and password1 == password2:
            user.set_password(password1)
            return {
                'success': u'Ваш пароль был успешно изменён'
            }
        else:
            return {
                'error': u'Введённые пароли не совпадают'
            }
    except:
        return {
            'error': u'Произошла ошибка. Обновите страницу и попробуйте ещё раз'
        }
