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


@login_required()
def cabinet_view(request):
    context = {}
    # user = User.objects.get(id=request.user.id)
    # if user.type == 1:
    #     city_qs = City.objects.all()[:10]
    #     client_qs = Client.objects.all()[:10]
    #     adjuster_qs = None
    # elif user.type == 2:
    #     city_qs = City.objects.filter(moderator=user)
    #     client_qs = Client.objects.filter(city__moderator=user)[:10]
    #     adjuster_qs = Adjuster.objects.filter(city__moderator=user)[:10]
    # else:
    #     city_qs = None
    #     client_qs = None
    #     adjuster_qs = None
    # if city_qs:
    #     context.update({
    #         'city_list': city_qs
    #     })
    # if client_qs:
    #     context.update({
    #         'client_list': client_qs
    #     })
    # if adjuster_qs:
    #     context.update({
    #         'adjuster_list': adjuster_qs
    #     })


    return render(request, 'cabinet_index.html', context)


# @ajax_request
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
