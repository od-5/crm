# coding=utf-8
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, CreateView
from apps.cabinet.forms import UserAddForm
from apps.city.models import City
from apps.client.forms import ClientUserUpdateForm, ClientUpdateForm, ClientUserAddForm, ClientAddForm, \
    ClientSurfaceAddForm, ClientMaketAddForm
from core.models import User
from .models import Client

__author__ = 'alexy'


def client_add(request):
    context = {}
    if request.method == "POST":
        user_form = ClientUserAddForm(request.POST)
        client_form = ClientAddForm(request.POST, request=request)
        if user_form.is_valid() and client_form.is_valid():
            user = user_form.save()
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
        if self.request.user.type == 1:
            qs = Client.objects.all()
        elif self.request.user.type == 2:
            qs = Client.objects.filter(city__moderator=user_id)
        else:
            qs = None
        queryset = qs
        if self.request.GET.get('email'):
            queryset = qs.filter(user__email=self.request.GET.get('email'))
        elif self.request.GET.get('legal_name'):
            queryset = qs.filter(legal_name=self.request.GET.get('legal_name'))
        else:
            if self.request.GET.get('city') and int(self.request.GET.get('city')) != 0:
                queryset = qs.filter(city__id=int(self.request.GET.get('city')))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ClientListView, self).get_context_data(**kwargs)
        user_id = self.request.user.id
        if self.request.user.type == 1:
            city_qs = City.objects.all()
        elif self.request.user.type == 2:
            city_qs = City.objects.filter(moderator=user_id)
        else:
            city_qs = None
        context.update({
            'city_list': city_qs
        })
        if self.request.GET.get('city'):
            context.update({
                'city_id': int(self.request.GET.get('city'))
            })
        return context


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

    client_surface_form = ClientSurfaceAddForm(
        initial={
            'client': client
        }
    )
    client_surface_form.fields['surface'].queryset = client.city.surface_set.all()
    client_maket_form = ClientMaketAddForm(
        initial={
            'client': client
        }
    )

    context.update({
        'success': success_msg,
        'error': error_msg,
        'user_form': user_form,
        'client_form': client_form,
        'client_surface_form': client_surface_form,
        'client_maket_form': client_maket_form,
        'object': client
    })
    return render(request, 'client/client_update.html', context)


def add_client_surface(request):
    if request.method == 'POST':
        print request.POST
    #     form = ClientSurfaceAddForm(request.POST)
    #     if form.is_valid():
    #         # file is saved
    #         print form
    #         # form.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def add_client_maket(request):
    if request.method == 'POST':
        form = ClientMaketAddForm(request.POST, request.FILES)
        if form.is_valid():
            # file is saved
            form.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
