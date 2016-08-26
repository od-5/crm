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
import datetime
from django.utils.timezone import utc
from apps.manager.models import Manager
from core.models import User

__author__ = 'alexy'


def manager_dashboard(user):
    manager = Manager.objects.get(user=user)
    return manager


@login_required()
def cabinet_view(request):
    context = {}
    user = request.user
    if user.type == 1:
        template_name = 'cabinet/dash_admin.html'
    elif user.type == 2 or user.type == 6:
        template_name = 'cabinet/dash_moderator.html'
    elif user.type == 3:
        return HttpResponseRedirect(reverse('surface:photo-list'))
    elif user.type == 4:
        return HttpResponseRedirect(reverse('adjustertask:list'))
    elif user.type == 5:
        manager = manager_dashboard(user)
        if manager.leader:
            template_name = 'cabinet/dash_moderator.html'
        else:
            template_name = 'cabinet/dash_manager.html'
        today = datetime.datetime.utcnow().replace(tzinfo=utc).date()
        actual_task_count = manager.incomingtask_set.filter(date=today).count()
        context.update({
            'manager': manager,
            'actual_task_count': actual_task_count
        })
        # print 'manager = %s' % manager
    else:
        raise Http404
    return render(request, template_name, context)


def cabinet_login(request):
    error = None
    if request.method == "POST":
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
    return render(request, 'sign/login.html', context)


class UserUpdateView(UpdateView):
    model = User
    template_name = 'cabinet/profile.html'
    form_class = UserProfileForm
    success_url = '/cabinet/profile/'

    def get_template_names(self):
        if self.request.user.type == 3 and self.request.session['is_mobile']:
            return 'mobile/profile_mobile.html'
        else:
            return 'core/profile.html'

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
            user.save()
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
