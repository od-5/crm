# coding=utf-8
from annoying.decorators import ajax_request
from django.shortcuts import render
from django.views.generic import ListView, CreateView
from apps.city.models import City
from core.models import User
from .models import Adjuster

__author__ = 'alexy'


class AdjusterListView(ListView):
    model = Adjuster

    def get_queryset(self):
        user_id = self.request.user.id
        print user_id
        if self.request.user.type == 1:
            qs = Adjuster.objects.all()
        elif self.request.user.type == 2:
            qs = Adjuster.objects.filter(city__moderator=user_id)
        else:
            qs = None
        queryset = qs
        return queryset


def adjuster_add(request):
    user = request.user
    if user.type == 1:
        city_list = City.objects.all()
    elif user.type == 2:
        city_list = City.objects.filter(moderator=user.id)
    context = {
        'city_list': city_list
    }
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            User.objects.get(email=email)
            context.update({
                'error': u'Такой пользователь уже зарегистрирован!'
            })
        except:
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            last_name = request.POST.get('last_name')
            first_name = request.POST.get('first_name')
            patronymic = request.POST.get('patronymic')
            if password1 and password2 and password1 == password2:
                pass
                new_user = User.objects.create_user(
                    email,
                    password1,
                    type=4,
                    last_name=last_name,
                    first_name=first_name,
                    patronymic=patronymic
                )
                context.update({
                    'success': u'Пользователь успешно создан!'
                })
                city_id = request.POST.get('city')
                city = City.objects.get(pk=int(city_id))

                adjuster = Adjuster.objects.create(
                    user=new_user,
                    city=city,
                )
                print '*'*10
                print adjuster
                print '*'*10
            else:
                context.update({
                    'error': u'Пароль и подтверждение пароля не совпадают!'
                })
    else:
        print 'NO ***'*5

    return render(request, 'adjuster/user_form.html', context)


def adjuster_update(request, pk):
    user = request.user
    adjuster_id = int(pk)
    adjuster = Adjuster.objects.get(pk=adjuster_id)

    if user.type == 1:
        city_list = City.objects.all()
    elif user.type == 2:
        city_list = City.objects.filter(moderator=user.id)
    context = {
        'object': adjuster,
        'city_list': city_list
    }

    adjuster_user = User.objects.get(adjuster=adjuster)
    print adjuster_user

    if request.method == 'POST':
        success_message = u''
        msg = None
        city_id = int(request.POST.get('city'))
        city = City.objects.get(pk=city_id)
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        last_name = request.POST.get('last_name')
        first_name = request.POST.get('first_name')
        patronymic = request.POST.get('patronymic')
        if password1 and password2:
            if password1 == password2:
                adjuster_user.set_password(password1)
                success_message += u'Пароль успешно изменен. '
            else:
                context.update({
                    'error': u'Пароль и подтверждение пароля не совпадают'
                })
        if adjuster_user.email != email:
            adjuster_user.email = email
            msg = u'Данные успешно изменены. '
        if adjuster_user.last_name != last_name:
            adjuster_user.last_name = last_name
            msg = u'Данные успешно изменены. '
        if adjuster_user.first_name != first_name:
            adjuster_user.first_name = first_name
            msg = u'Данные успешно изменены. '
        if adjuster_user.patronymic != patronymic:
            adjuster_user.patronymic = patronymic
            msg = u'Данные успешно изменены. '
        adjuster_user.save()

        if adjuster.city.id != city_id:
            adjuster.city = city
            adjuster.save()

        if msg:
            success_message += msg
        context.update({
            'success': success_message
        })
    # print adjuster.user.email
    # print adjuster.user.first_name
    # print adjuster.user.last_name
    # print adjuster.user.patronymic
    return render(request, 'adjuster/adjuster_update.html', context)
