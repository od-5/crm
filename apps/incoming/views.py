# coding=utf-8
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from datetime import datetime
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.utils import timezone
from apps.city.models import City
from apps.manager.models import Manager
from .models import IncomingClient, IncomingTask, IncomingClientContact, IncomingClientManager
from .forms import IncomingClientAddForm, IncomingClientUpdateForm, IncomingTaskForm, IncomingClientContactForm, \
    IncomingClientImportForm

__author__ = 'alexy'


class IncomingClientListView(ListView):
    model = IncomingClient
    template_name = 'incoming/incoming_list.html'
    paginate_by = 25

    def get_paginate_by(self, queryset):
        """
        Получение параметра - сколько показывать элементов на странице
        """
        if self.request.GET.get('page_count'):
            if self.request.GET.get('page_count') == '0':
                page_count = 0
            else:
                page_count = int(self.request.GET.get('page_count'))
        else:
            try:
                page_count = int(self.request.session['page_count'])
            except:
                page_count = self.paginate_by
        self.paginate_by = self.request.session['page_count'] = page_count
        return page_count

    def get_queryset(self):
        user = self.request.user
        name = self.request.GET.get('name')
        phone = self.request.GET.get('phone')
        contact = self.request.GET.get('contact')
        manager = self.request.GET.get('manager')
        city = self.request.GET.get('city')
        print('city', city)
        if user.type == 1:
            qs = IncomingClient.objects.select_related().all()
        elif user.type == 6:
            qs = IncomingClient.objects.select_related().filter(city__moderator__in=user.superviser.moderator_id_list())
        elif user.type == 2:
            qs = IncomingClient.objects.select_related().filter(city__moderator=user)
        elif user.type == 5:
            if user.is_leader_manager():
                qs = IncomingClient.objects.select_related().filter(city__moderator=user.manager.moderator)
            else:
                qs = IncomingClient.objects.select_related().filter(manager__user=user)
        else:
            qs = None
        if name:
            qs = qs.filter(name__icontains=name)
        if phone or name:
            client_id_list = [int(i.id) for i in qs]
            c_qs = IncomingClientContact.objects.select_related().filter(incomingclient__in=client_id_list)
            if phone:
                c_qs = c_qs.filter(phone=phone)
            if contact:
                c_qs = c_qs.filter(name__icontains=contact)
            client_id_list = [int(i.incomingclient.id) for i in c_qs]
            qs = qs.filter(id__in=client_id_list)
        if manager and int(manager) != 0:
            qs = qs.filter(manager=int(manager))
        if city and int(city) != 0:
            qs = qs.filter(city=int(city))
        return qs.select_related('city').prefetch_related('incomingtask_set')

    def get_context_data(self, **kwargs):
        context = super(IncomingClientListView, self).get_context_data(**kwargs)
        if self.request.GET.get('name'):
            context.update({
                'r_name': self.request.GET.get('name')
            })
        if self.request.GET.get('phone'):
            context.update({
                'r_phone': self.request.GET.get('phone')
            })
        if self.request.GET.get('contact'):
            context.update({
                'r_contact': self.request.GET.get('contact')
            })
        if self.request.GET.get('manager'):
            context.update({
                'r_manager': int(self.request.GET.get('manager'))
            })
        if self.request.GET.get('city'):
            context.update({
                'r_city': int(self.request.GET.get('city'))
            })
        queryset = self.object_list
        manager_client_count = queryset.count()
        manager_task_count = 0
        search_client_name = self.request.GET.get('client_name')
        if search_client_name:
            if self.request.user.type == 5:
                qs = IncomingClient.objects.filter(city__moderator=self.request.user.manager.moderator)
            else:
                qs = queryset
            search_client_qs = qs.filter(name__icontains=search_client_name)
            context.update({
                'search_client_list': search_client_qs,
                'r_client_name': search_client_name
            })
        for client in queryset:
            manager_task_count += client.incomingtask_set.count()
        context.update({
            'manager_client_count': manager_client_count,
            'manager_task_count': manager_task_count
        })
        user = self.request.user
        if user.type == 5:
            context.update({
                'current_manager': user.manager
            })
        import_form = IncomingClientImportForm()
        if self.request.META['QUERY_STRING']:
            self.request.session['incoming_filtered_list'] = '%s?%s' % (self.request.path, self.request.META['QUERY_STRING'])
        else:
            self.request.session['incoming_filtered_list'] = reverse('incoming:list')
        context.update({
            'import_form': import_form,
            'manager_list': Manager.objects.get_qs(user),
            'city_list': City.objects.get_qs(user),
            'page_count': self.paginate_by,
        })
        return context


@login_required
def incomingclient_add(request):
    context = {}
    initial = {}
    user = request.user
    if user.type == 1:
        manager_qs = Manager.objects.all()
        city_qs = City.objects.all()
    elif user.type == 6:
        manager_qs = Manager.objects.filter(moderator__in=user.superviser.moderator_id_list(), user__is_active=True)
        city_qs = user.superviser.city.all()
    elif user.type == 2:
        manager_qs = Manager.objects.filter(moderator=user)
        city_qs = City.objects.filter(moderator=user)
    elif user.type == 5:
        manager = Manager.objects.get(user=user)
        manager_qs = Manager.objects.filter(moderator=manager.moderator)
        city_qs = City.objects.filter(moderator=manager.moderator)
        if not user.is_leader_manager():
            initial = {
                'manager': manager
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
    try:
        request.session['incoming_filtered_list']
    except:
        request.session['incoming_filtered_list'] = reverse('incoming:list')
    context.update({
        'form': form,
        'back_to_list': request.session['incoming_filtered_list']
    })
    return render(request, 'incoming/incoming_add.html', context)


@login_required
def incomingclient_update(request, pk):
    context = {}
    incomingclient = IncomingClient.objects.get(pk=int(pk))
    old_manager_id = incomingclient.manager.id
    success_msg = u''
    error_msg = u''
    user = request.user
    if user.type == 1:
        manager_qs = Manager.objects.all()
        city_qs = City.objects.all()
    elif user.type == 6:
        manager_qs = Manager.objects.filter(moderator__in=user.superviser.moderator_id_list(), user__is_active=True)
        city_qs = user.superviser.city.all()
    elif user.type == 2:
        manager_qs = Manager.objects.filter(moderator=user)
        city_qs = City.objects.filter(moderator=user)
    elif user.type == 5:
        manager = Manager.objects.get(user=user)
        manager_qs = Manager.objects.filter(moderator=manager.moderator)
        city_qs = City.objects.filter(moderator=manager.moderator)
    else:
        manager_qs = None
        city_qs = None
    if request.method == 'POST':
        form = IncomingClientUpdateForm(request.POST, instance=incomingclient)
        if form.is_valid():
            incoming = form.save(commit=False)
            incoming.save()
            if old_manager_id != incoming.manager.id:
                incoming.type = 2
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
    try:
        request.session['incoming_filtered_list']
    except:
        request.session['incoming_filtered_list'] = reverse('incoming:list')
    context.update({
        'success': success_msg,
        'error': error_msg,
        'form': form,
        'object': incomingclient,
        'back_to_list': request.session['incoming_filtered_list']
    })
    return render(request, 'incoming/incoming_update.html', context)


@login_required
def incomingclientcontact_history(request, pk):
    incomingclient = IncomingClient.objects.get(pk=int(pk))
    try:
        request.session['incoming_filtered_list']
    except:
        request.session['incoming_filtered_list'] = reverse('incoming:list')
    context = {
        'object': incomingclient,
        'object_list': incomingclient.incomingclientmanager_set.all(),
        'back_to_list': request.session['incoming_filtered_list']
    }
    return render(request, 'incoming/incomingclientcontact_history.html', context)


@login_required
def incomingclientcontact_list(request, pk):
    incomingclient = IncomingClient.objects.get(pk=int(pk))
    try:
        request.session['incoming_filtered_list']
    except:
        request.session['incoming_filtered_list'] = reverse('incoming:list')
    context = {
        'object': incomingclient,
        'object_list': incomingclient.incomingclientcontact_set.all(),
        'back_to_list': request.session['incoming_filtered_list']
    }
    return render(request, 'incoming/incomingclientcontact_list.html', context)


@login_required
def incomingclientcontact_add(request, pk):
    success_msg = None
    error_msg = None
    incomingclient = IncomingClient.objects.get(pk=int(pk))
    if request.method == 'POST':
        form = IncomingClientContactForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('incoming:contact-list', args=(incomingclient.id,)))
        else:
            error_msg = u'Проверьте правильность ввода полей!'
    else:
        form = IncomingClientContactForm(
            initial={
                'incomingclient': incomingclient
            }
        )
    try:
        request.session['incoming_filtered_list']
    except:
        request.session['incoming_filtered_list'] = reverse('incoming:list')
    context = {
        'object': incomingclient,
        'form': form,
        'success_msg': success_msg,
        'error_msg': error_msg,
        'back_to_list': request.session['incoming_filtered_list']
    }
    return render(request, 'incoming/incomingclientcontact_add.html', context)


@login_required
def incomingclientcontact_update(request, pk):
    success_msg = None
    error_msg = None
    contact = IncomingClientContact.objects.get(pk=int(pk))
    if request.method == 'POST':
        form = IncomingClientContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('incoming:contact-list', args=(contact.incomingclient.id,)))
        else:
            error_msg = u'Проверьте правильность ввода полей!'
    else:
        form = IncomingClientContactForm(instance=contact)
    try:
        request.session['incoming_filtered_list']
    except:
        request.session['incoming_filtered_list'] = reverse('incoming:list')
    context = {
        'contact': contact,
        'object': contact.incomingclient,
        'form': form,
        'success_msg': success_msg,
        'error_msg': error_msg,
        'back_to_list': request.session['incoming_filtered_list']
    }
    return render(request, 'incoming/incomingclientcontact_update.html', context)


@login_required
def incomingtask_list(request):
    context = {}
    if request.GET.get('error') and int(request.GET.get('error')) == 1:
        context.update({
            'error': True
        })
    user = request.user
    if user.type == 1:
        qs = IncomingTask.objects.all()
        manager_qs = Manager.objects.all()
    elif user.type == 2:
        qs = IncomingTask.objects.filter(manager__moderator=user)
        manager_qs = Manager.objects.filter(moderator=user)
    elif user.type == 6:
        qs = IncomingTask.objects.filter(manager__moderator__in=user.superviser.moderator_id_list())
        manager_qs = Manager.objects.filter(moderator__in=user.superviser.moderator_id_list())
    elif user.type == 5:
        manager_qs = Manager.objects.filter(moderator=user.manager.moderator)
        if user.is_leader_manager():
            qs = IncomingTask.objects.filter(manager__moderator=user.manager.moderator)
        else:
            qs = IncomingTask.objects.filter(manager__user=user)
    else:
        qs = manager_qs = None
    r_manager = request.GET.get('r_manager')
    r_name = request.GET.get('name')
    r_date_s = request.GET.get('date_s')
    r_date_e = request.GET.get('date_e')
    r_all = request.GET.get('all')
    r_type = request.GET.get('type')
    r_status = request.GET.get('status')
    if r_all and int(r_all) == 1:
        request.session['show_all_incomingtask'] = True
    elif r_all and int(r_all) == 0:
        request.session['show_all_incomingtask'] = False
    try:
        show_all = request.session['show_all_incomingtask']
    except:
        show_all = False
    if not r_name and not r_date_s and not r_date_e and not show_all:
        qs = qs.filter(date=timezone.localtime(timezone.now()))
    else:
        if r_name:
            qs = qs.filter(incomingclient__name__icontains=r_name)
        if r_date_s:
            qs = qs.filter(date__gte=datetime.strptime(r_date_s, '%d.%m.%Y'))
        if r_date_e:
            qs = qs.filter(date__lte=datetime.strptime(r_date_e, '%d.%m.%Y'))
    if r_manager and int(r_manager) != 0:
        qs = qs.filter(manager=int(r_manager))
        context.update({
            'r_manager': int(r_manager)
        })
    if r_type:
        qs = qs.filter(type=int(r_type))
        context.update({
            'r_type': True
        })
    if r_status:
        qs = qs.filter(status=int(r_status))
        context.update({
            'r_status': int(r_status)
        })
    if r_name:
        context.update({
            'r_name': r_name
        })
    if r_date_s:
        context.update({
            'r_date_s': r_date_s
        })
    if r_date_e:
        context.update({
            'r_date_e': r_date_e
        })
    if show_all:
        context.update({
            'show_all': True
        })

    page_count = 25
    if request.GET.get('page_count'):
        if request.GET.get('page_count') == '0':
            page_count = 0
        else:
            page_count = int(request.GET.get('page_count'))
    else:
        try:
            page_count = int(request.session['page_count'])
        except:
            pass
    request.session['page_count'] = page_count
    paginator = Paginator(qs, page_count)
    page = request.GET.get('page')
    try:
        object_list = paginator.page(page)
    except (PageNotAnInteger, ZeroDivisionError):
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)
    if request.META['QUERY_STRING']:
        request.session['incomingtask_filtered_list'] = '%s?%s' % (request.path, request.META['QUERY_STRING'])
    else:
        request.session['incomingtask_filtered_list'] = reverse('incoming:task-list')
    context.update({
        'object_list': object_list,
        'manager_list': manager_qs,
        'page_count': page_count
    })
    return render(request, 'incoming/incomingtask_list.html', context)


@login_required
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
    elif user.type == 6:
        manager_qs = Manager.objects.filter(moderator__in=user.superviser.moderator_id_list(), user__is_active=True)
        incomingclient_qs = IncomingClient.objects.filter(manager__moderator__in=user.superviser.moderator_id_list())
    elif user.type == 5:
        manager = Manager.objects.get(user=user)
        manager_qs = Manager.objects.filter(moderator=manager.moderator)
        if user.is_leader_manager():
            incomingclient_qs = IncomingClient.objects.filter(manager__moderator=manager.moderator)
        else:
            incomingclient_qs = IncomingClient.objects.filter(manager=manager)
            initial = {
                'manager': manager
            }
    else:
        manager_qs = None
        incomingclient_qs = None
    if request.method == "POST":
        form = IncomingTaskForm(request.POST, initial=initial)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return HttpResponseRedirect(reverse('incoming:task-update', args=(instance.id,)))
        else:
            context.update({
                'error': u'Проверьте правильность ввода полей'
            })
    else:
        form = IncomingTaskForm(initial=initial)
    form.fields['manager'].queryset = manager_qs
    form.fields['incomingclient'].queryset = incomingclient_qs
    try:
        request.session['incomingtask_filtered_list']
    except:
        request.session['incomingtask_filtered_list'] = reverse('incoming:task-list')
    context.update({
        'form': form,
        'back_to_list': request.session['incomingtask_filtered_list']
    })
    return render(request, 'incoming/incomingtask_add.html', context)


@login_required
def incomingtask_update(request, pk):
    context = {}
    object = IncomingTask.objects.get(pk=int(pk))
    success_msg = u''
    error_msg = u''
    user = request.user
    if user.type == 1:
        manager_qs = Manager.objects.all()
    elif user.type == 6:
        manager_qs = Manager.objects.filter(moderator__in=user.superviser.moderator_id_list(), user__is_active=True)
    elif user.type == 2:
        manager_qs = Manager.objects.filter(moderator=user)
    elif user.type == 5:
        manager = Manager.objects.get(user=user)
        manager_qs = Manager.objects.filter(moderator=manager.moderator)
    else:
        manager_qs = None
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
    form.fields['incomingclientcontact'].queryset = object.incomingclient.incomingclientcontact_set.all()
    try:
        request.session['incomingtask_filtered_list']
    except:
        request.session['incomingtask_filtered_list'] = reverse('incoming:task-list')
    context.update({
        'success': success_msg,
        'error': error_msg,
        'form': form,
        'object': object,
        'back_to_list': request.session['incomingtask_filtered_list']
    })
    return render(request, 'incoming/incomingtask_update.html', context)
