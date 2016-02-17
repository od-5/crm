# coding=utf-8
import datetime
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import xlwt
from datetime import date, datetime
from annoying.decorators import ajax_request
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.utils import timezone
from apps.city.models import City
from apps.manager.models import Manager
from core.forms import UserAddForm, UserUpdateForm
from core.models import User
from .models import IncomingClient, IncomingTask, IncomingClientContact, IncomingClientManager
from .forms import IncomingClientAddForm, IncomingClientUpdateForm, IncomingTaskForm, IncomingClientContactForm

__author__ = 'alexy'


class IncomingClientListView(ListView):
    model = IncomingClient
    template_name = 'incoming/incoming_list.html'
    paginate_by = 25

    def get_queryset(self):
        user = self.request.user
        if user.type == 1:
            qs = IncomingClient.objects.all()
        elif user.type == 2:
            qs = IncomingClient.objects.filter(city__moderator=user)
        elif user.type == 5:
            qs = IncomingClient.objects.filter(manager=user)
        else:
            qs = None
        if self.request.GET.get('name'):
            qs = qs.filter(name__icontains=self.request.GET.get('name'))
        return qs

    def get_context_data(self, **kwargs):
        context = super(IncomingClientListView, self).get_context_data(**kwargs)
        if self.request.GET.get('name'):
            context.update({
                'r_name': self.request.GET.get('name')
            })
        return context


def incomingclient_add(request):
    context = {}
    initial = {}
    user = request.user
    if user.type == 1:
        manager_qs = Manager.objects.all()
        city_qs = City.objects.all()
    elif user.type == 2:
        manager_qs = Manager.objects.filter(moderator=user)
        city_qs = City.objects.filter(moderator=user)
    elif user.type == 5:
        user_manager = Manager.objects.get(user=user)
        manager_qs = Manager.objects.filter(moderator=user_manager.moderator)
        city_qs = City.objects.filter(moderator=user_manager.moderator)
        initial = {
            'manager': user_manager
        }
    else:
        manager_qs = None
        city_qs = None
    if request.method == "POST":
        form = IncomingClientAddForm(request.POST)
        if form.is_valid():
            incoming = form.save(commit=False)
            incoming.save()
            incomingclientmanager = IncomingClientManager(manager=incoming.manager, incomingclient=incoming)
            incomingclientmanager.save()
            return HttpResponseRedirect(reverse('incoming:update', args=(incoming.id,)))
        else:
            context.update({
                'error': u'Проверьте правильность ввода полей'
            })
    else:
        form = IncomingClientAddForm(initial=initial)
    form.fields['manager'].queryset = manager_qs
    form.fields['city'].queryset = city_qs
    context.update({
        'form': form,
    })
    return render(request, 'incoming/incoming_add.html', context)


def incomingclient_update(request, pk):
    context = {}
    incomingclient = IncomingClient.objects.get(pk=int(pk))
    success_msg = u''
    error_msg = u''
    user = request.user
    if user.type == 1:
        manager_qs = Manager.objects.all()
        city_qs = City.objects.all()
    elif user.type == 2:
        manager_qs = Manager.objects.filter(moderator=user)
        city_qs = City.objects.filter(moderator=user)
    elif user.type == 5:
        manager_qs = Manager.objects.filter(moderator=user.moderator)
        city_qs = City.objects.filter(moderator=user.moderator)
    else:
        manager_qs = None
        city_qs = None
    if request.method == 'POST':
        form = IncomingClientUpdateForm(request.POST, instance=incomingclient)
        if form.is_valid():
            incoming = form.save(commit=False)
            incoming.save()
            incomingclientmanager = IncomingClientManager(manager=incoming.manager, incomingclient=incoming)
            incomingclientmanager.save()
            success_msg = u' Изменения успешно сохранены'
        else:
            error_msg = u'Проверьте правильность ввода полей!'
    else:
        form = IncomingClientUpdateForm(instance=incomingclient)

    form.fields['manager'].queryset = manager_qs
    form.fields['city'].queryset = city_qs

    context.update({
        'success': success_msg,
        'error': error_msg,
        'form': form,
        'object': incomingclient,
    })
    return render(request, 'incoming/incoming_update.html', context)


def incomingclientcontact_history(request, pk):
    incomingclient = IncomingClient.objects.get(pk=int(pk))
    context = {
        'object': incomingclient,
        'object_list': incomingclient.incomingclientmanager_set.all()
    }
    return render(request, 'incoming/incomingclientcontact_history.html', context)


def incomingclientcontact_list(request, pk):
    incomingclient = IncomingClient.objects.get(pk=int(pk))
    context = {
        'object': incomingclient,
        'object_list': incomingclient.incomingclientcontact_set.all()
    }
    return render(request, 'incoming/incomingclientcontact_list.html', context)


def incomingclientcontact_add(request, pk):
    context = {}
    success_msg = None
    error_msg = None
    incomingclient = IncomingClient.objects.get(pk=int(pk))
    if request.method == 'POST':
        form = IncomingClientContactForm(request.POST)
        if form.is_valid():
            form.save()
            success_msg = u'Контактное лицо успешно добавлено'
            return HttpResponseRedirect(reverse('incoming:contact-list', args=(incomingclient.id,)))
        else:
            error_msg = u'Проверьте правильность ввода полей!'
    else:
        form = IncomingClientContactForm(
            initial={
                'incomingclient': incomingclient
            }
        )
    context = {
        'object': incomingclient,
        'form': form,
        'success_msg': success_msg,
        'error_msg': error_msg
    }
    return render(request, 'incoming/incomingclientcontact_add.html', context)


def incomingclientcontact_update(request, pk):
    context = {}
    success_msg = None
    error_msg = None
    contact = IncomingClientContact.objects.get(pk=int(pk))
    if request.method == 'POST':
        form = IncomingClientContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            success_msg = u'Изменения сохранены'
            return HttpResponseRedirect(reverse('incoming:contact-list', args=(contact.incomingclient.id,)))
        else:
            error_msg = u'Проверьте правильность ввода полей!'
    else:
        form = IncomingClientContactForm(instance=contact)
    context = {
        'contact': contact,
        'object': contact.incomingclient,
        'form': form,
        'success_msg': success_msg,
        'error_msg': error_msg
    }
    return render(request, 'incoming/incomingclientcontact_update.html', context)


class IncomingTaskListView(ListView):
    model = IncomingTask
    template_name = 'incoming/incomingtask_list.html'
    paginate_by = 25

    def get_queryset(self):
        user = self.request.user

        if user.type == 1:
            qs = IncomingTask.objects.all()
        elif user.type == 2:
            qs = IncomingTask.objects.filter(manager__moderator=user)
        elif user.type == 5:
            qs = IncomingTask.objects.filter(manager=user)
        else:
            qs = None
        r_name = self.request.GET.get('name')
        r_date_s = self.request.GET.get('date_s')
        r_date_e = self.request.GET.get('date_e')
        r_all = self.request.GET.get('all')
        if not r_name and not r_date_s and not r_date_e and not r_all:
            qs = qs.filter(date=timezone.localtime(timezone.now()))
            print 'TODAY'
        else:
            if r_name:
                qs = qs.filter(incomingclient__name__icontains=r_name)
            if r_date_s:
                qs = qs.filter(date__gte=datetime.strptime(r_date_s, '%d.%m.%Y'))
            if r_date_e:
                qs = qs.filter(date__lte=datetime.strptime(r_date_e, '%d.%m.%Y'))
            print "FILTERED INPUT"

        return qs

    def get_context_data(self, **kwargs):
        context = super(IncomingTaskListView, self).get_context_data(**kwargs)
        if self.request.GET.get('name'):
            context.update({
                'r_name': self.request.GET.get('name')
            })
        if self.request.GET.get('date_s'):
            context.update({
                'r_date_s': self.request.GET.get('date_s')
            })
        if self.request.GET.get('date_e'):
            context.update({
                'r_date_e': self.request.GET.get('date_e')
            })
        if self.request.GET.get('all'):
            context.update({
                'show_all': True
            })
        return context


def incomingtask_add(request):
    context = {}
    initial = {}
    user = request.user
    if user.type == 1:
        manager_qs = Manager.objects.all()
        incomingclient_qs = IncomingClient.objects.all()
    elif user.type == 2:
        manager_qs = Manager.objects.filter(moderator=user)
        incomingclient_qs = IncomingClient.objects.filter(manager__moderator=user)
    elif user.type == 5:
        manager_qs = Manager.objects.filter(moderator=user.moderator)
        incomingclient_qs = IncomingClient.objects.filter(manager=user)
        initial = {
            'manager': user
        }
    else:
        manager_qs = None
        incomingclient_qs = None
    if request.method == "POST":
        form = IncomingTaskForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return HttpResponseRedirect(reverse('incoming:task-update', args=(instance.id,)))
        else:
            context.update({
                'error': u'Проверьте правильность ввода полей'
            })
    else:
        form = IncomingTaskForm()
    form.fields['manager'].queryset = manager_qs
    form.fields['incomingclient'].queryset = incomingclient_qs
    context.update({
        'form': form,
    })
    return render(request, 'incoming/incomingtask_add.html', context)


def incomingtask_update(request, pk):
    context = {}
    object = IncomingTask.objects.get(pk=int(pk))
    success_msg = u''
    error_msg = u''
    user = request.user
    if user.type == 1:
        manager_qs = Manager.objects.all()
        incomingclient_qs = IncomingClient.objects.all()
    elif user.type == 2:
        manager_qs = Manager.objects.filter(moderator=user)
        incomingclient_qs = IncomingClient.objects.filter(manager__moderator=user)
    elif user.type == 5:
        manager_qs = Manager.objects.filter(moderator=user.moderator)
        incomingclient_qs = IncomingClient.objects.filter(manager=user)
    else:
        manager_qs = None
        incomingclient_qs = None
    if request.method == 'POST':
        form = IncomingTaskForm(request.POST, instance=object)
        if form.is_valid():
            form.save()
            success_msg = u' Изменения успешно сохранены'
        else:
            error_msg = u'Проверьте правильность ввода полей!'
    else:
        form = IncomingTaskForm(instance=object)

    form.fields['manager'].queryset = manager_qs
    form.fields['incomingclient'].queryset = incomingclient_qs

    context.update({
        'success': success_msg,
        'error': error_msg,
        'form': form,
        'object': object,
    })
    return render(request, 'incoming/incomingtask_update.html', context)
