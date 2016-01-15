# coding=utf-8
import datetime

import xlwt
from annoying.decorators import ajax_request
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from apps.city.models import City, Surface
from apps.client.forms import ClientUpdateForm, ClientAddForm, ClientSurfaceAddForm, ClientMaketForm, ClientOrderForm, \
    ClientJournalForm
from core.forms import UserAddForm, UserUpdateForm
from .models import Client, ClientSurface, ClientMaket, ClientOrder, ClientOrderSurface

__author__ = 'alexy'


def client_add(request):
    context = {}
    if request.method == "POST":
        user_form = UserAddForm(request.POST)
        client_form = ClientAddForm(request.POST, request=request)
        if user_form.is_valid() and client_form.is_valid():
            user = user_form.save(commit=False)
            user.type = 3
            user.save()
            client = client_form.save(commit=False)
            client.user = user
            client.save()
            return HttpResponseRedirect(reverse('client:change', args=(client.id, )))
        else:
            context.update({
                'error': u'Проверьте правильность ввода полей'
            })
    else:
        user_form = UserAddForm()
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
        user_form = UserUpdateForm(request.POST, instance=user)
        client_form = ClientUpdateForm(request.POST, request=request, instance=client)
        if user_form.is_valid() and client_form.is_valid():
            user_form.save()
            client_form.save()
            success_msg += u' Изменения успешно сохранены'
        else:
            error_msg = u'Проверьте правильность ввода полей!'
    else:
        user_form = UserUpdateForm(instance=user)
        client_form = ClientUpdateForm(request=request, instance=client)

    context.update({
        'success': success_msg,
        'error': error_msg,
        'user_form': user_form,
        'client_form': client_form,
        'object': client,
        'client': client,
    })
    return render(request, 'client/client_update.html', context)


def client_maket(request, pk):
    context = {}
    client = Client.objects.get(pk=int(pk))
    success_msg = u''
    error_msg = u''
    client_maket_form = ClientMaketForm(
        initial={
            'client': client
        }
    )

    context.update({
        'success': success_msg,
        'error': error_msg,
        'client_maket_form': client_maket_form,
        'object': client,
        'client': client,
    })
    return render(request, 'client/client_maket.html', context)


def client_maket_update(request, pk):
    context = {}
    maket = ClientMaket.objects.get(pk=int(pk))
    success_msg = u''
    error_msg = u''
    if request.method == 'POST':
        form = ClientMaketForm(request.POST, request.FILES, instance=maket)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('client:maket', args=(maket.client.id, )))
    else:
        form = ClientMaketForm(instance=maket, initial={
            'file': maket.file
        })
    context.update({
        'success': success_msg,
        'error': error_msg,
        'client_maket_form': form,
        'object': maket,
        'client': maket.client
    })
    return render(request, 'client/client_maket_update.html', context)


def client_order(request, pk):
    context = {}
    client = Client.objects.get(pk=int(pk))
    success_msg = u''
    error_msg = u''
    if request.method == 'POST':
        form = ClientOrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            return HttpResponseRedirect(reverse('client:order-update', args=(order.id, )))
    else:
        form = ClientOrderForm(initial={
            'client': client
        })
    context.update({
        'success': success_msg,
        'error': error_msg,
        'client_order_form': form,
        'object': client,
        'client': client
    })
    return render(request, 'client/client_order.html', context)


def client_order_update(request, pk):
    context = {}
    order = ClientOrder.objects.get(pk=int(pk))
    client = order.client
    area_list = client.city.area_set.all()
    success_msg = u''
    error_msg = u''

    if request.method == 'POST':
        form = ClientOrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
    else:
        form = ClientOrderForm(instance=order)
    context.update({
        'success': success_msg,
        'error': error_msg,
        'order_form': form,
        'object': order,
        'client': client,
        'area_list': area_list
    })
    return render(request, 'client/client_order_update.html', context)


def client_journal(request, pk):
    # TODO: Сделать страницу журнала покупок клиента
    context = {}
    client = Client.objects.get(pk=int(pk))
    success_msg = u''
    error_msg = u''
    if request.method == 'POST':
        form = ClientJournalForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('client:journal', args=(client.id, )))
    else:
        form = ClientJournalForm(initial={
            'client': client
        })
    form.fields['clientorder'].queryset = client.clientorder_set.all()
    context.update({
        'success': success_msg,
        'error': error_msg,
        'clientjournal_form': form,
        'object': client,
        'client': client
    })
    return render(request, 'client/client_journal.html', context)


# @ajax_request
def add_client_surface(request):
    print 'STEP 1'
    if request.method == 'POST':
        print 'STEP 2 - POST'
        # print request.POST
        # client = Client.objects.get(pk=int(request.POST.get('cos_client')))
        # print 'client %s' % int(request.POST.get('cos_client'))
        print 'client %s' % int(request.POST.get('cos_order'))
        order = ClientOrder.objects.get(pk=int(request.POST.get('cos_order')))
        surfaces = request.POST.getlist('chk_group[]')
        for item in surfaces:
            surface = Surface.objects.get(pk=int(item))
            surface.free = False
            surface.save()
            print surface
            c_surface = ClientOrderSurface(
                clientorder=order,
                surface=surface
            )
            c_surface.save()
        return HttpResponseRedirect(reverse('client:order-update', args=(int(request.POST.get('cos_order')),)))
        # return HttpResponseRedirect(reverse('client:order'))
    else:
        print 'STEP FAIL'
        return HttpResponseRedirect(reverse('client:order', args=(int(request.POST.get('cos_order')),)))


def client_maket_add(request):
    if request.method == 'POST':
        form = ClientMaketForm(request.POST, request.FILES)
        if form.is_valid():
            # file is saved
            form.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@ajax_request
@csrf_exempt
def remove_client_surface(request):
    if request.method == 'POST':
        if request.POST.get('client_surface_id'):
            client_surface = ClientSurface.objects.get(id=int(request.POST.get('client_surface_id')))
            client_surface.delete()
            return {
                'success': True
            }
        else:
            return {
                'error': True
            }


def client_excel_export(request, pk):
    client = Client.objects.get(id=int(pk))
    font0 = xlwt.Font()
    font0.name = 'Calibri'
    font0.height = 220

    borders = xlwt.Borders()
    borders.left = xlwt.Borders.THIN
    borders.right = xlwt.Borders.THIN
    borders.top = xlwt.Borders.THIN
    borders.bottom = xlwt.Borders.THIN

    style0 = xlwt.XFStyle()
    style0.font = font0

    style1 = xlwt.XFStyle()
    style1.font = font0
    style1.borders = borders

    wb = xlwt.Workbook()
    ws = wb.add_sheet(u'Рекламные поверхости')
    ws.write(0, 0, u'Клиент:', style0)
    ws.write(0, 1, u'%s' % client.legal_name, style0)
    ws.write(1, 0, u'Город:', style0)
    ws.write(1, 1, u'%s' % client.city.name, style0)

    ws.write(3, 0, u'Город', style1)
    ws.write(3, 1, u'Район', style1)
    ws.write(3, 2, u'Улица', style1)
    ws.write(3, 3, u'Номер дома', style1)
    ws.write(3, 4, u'Дата размещения', style1)
    ws.write(3, 5, u'Дата окончания размещения', style1)

    i = 4
    if client.clientsurface_set.all():
        for item in client.clientsurface_set.all():
            ws.write(i, 0, item.surface.city.name, style1)
            ws.write(i, 1, item.surface.street.area.name, style1)
            ws.write(i, 2, item.surface.street.name, style1)
            ws.write(i, 3, item.surface.house_number, style1)
            ws.write(i, 4, str(item.date_start), style1)
            ws.write(i, 5, str(item.date_end), style1)
            i += 1

    ws.col(0).width = 6666
    ws.col(1).width = 6666
    ws.col(2).width = 10000
    ws.col(3).width = 4500
    ws.col(4).width = 10000
    ws.col(5).width = 10000
    for count in range(i):
        ws.row(count).height = 300

    fname = 'client_#%d_address_list.xls' % client.id
    response = HttpResponse(content_type="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=%s' % fname
    wb.save(response)
    return response
