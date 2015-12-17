# coding=utf-8
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, CreateView
from apps.cabinet.forms import UserAddForm
from apps.client.forms import ClientUserUpdateForm, ClientUpdateForm, ClientUserAddForm, ClientAddForm
from core.models import User
from .models import Client

__author__ = 'alexy'


def client_add(request):
    context = {}
    if request.method == "POST":
        user_form = ClientUserAddForm(request.POST)
        client_form = ClientAddForm(request.POST, request=request)
        print '*'*10
        print u'До валидации'
        if user_form.is_valid() and client_form.is_valid():
            print '*'*10
            print u'Валидация пользователя'
            print user_form
            print client_form
            user = user_form.save()
            print user
            client = client_form.save(commit=False)
            client.user = user
            client.save()
            return HttpResponseRedirect(reverse('client:change', args=(client.id, )))
        else:
            context.update({
                'error': u'Проверьте правильность ввода полей'
            })
    else:
        user_form = ClientUserAddForm()
        client_form = ClientAddForm(request=request)
    context.update({
        'user_form': user_form,
        'client_form': client_form
    })
    return render(request, 'client/client_add.html', context)


class ClientListView(ListView):
    model = Client

    def get_queryset(self):
        user_id = self.request.user.id
        print user_id
        if self.request.user.type == 1:
            qs = Client.objects.all()
        elif self.request.user.type == 2:
            qs = Client.objects.filter(city__moderator=user_id)
        else:
            qs = None
        queryset = qs
        return queryset


def client_update(request, pk):
    context = {}
    client = Client.objects.get(pk=int(pk))
    user = client.user
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
        user_form = ClientUserUpdateForm(request.POST, instance=user)
        client_form = ClientUpdateForm(request.POST, request=request, instance=client)
        if user_form.is_valid() and client_form.is_valid():
            user_form.save()
            client_form.save()
            success_msg += u' Изменения успешно сохранены'
        else:
            error_msg = u'Проверьте правильность ввода полей!'
    else:
        user_form = ClientUserUpdateForm(instance=user)
        client_form = ClientUpdateForm(request=request, instance=client)
    context.update({
        'success': success_msg,
        'error': error_msg,
        'user_form': user_form,
        'client_form': client_form,
        'object': client
    })
    return render(request, 'client/client_update.html', context)
