# coding=utf-8
from annoying.functions import get_object_or_None
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView
from apps.city.models import City
from apps.manager.models import Manager
from apps.ticket.forms import TicketChangeForm
from .models import Ticket

__author__ = 'alexy'


class TicketListView(ListView):
    model = Ticket
    paginate_by = 25
    template_name = 'ticket/ticket_list.html'

    def get_queryset(self):
        user = self.request.user
        if user.type == 1:
            qs = Ticket.objects.all()
        elif user.type == 2:
            qs = Ticket.objects.filter(city__moderator=user)
        elif user.type == 5:
            manager = Manager.objects.get(user=user)
            qs = Ticket.objects.filter(city__moderator=manager.moderator)
        else:
            qs = None
        if self.request.GET.get('name'):
            qs = qs.filter(name=self.request.GET.get('name'))
        if self.request.GET.get('phone'):
            qs = qs.filter(phone=self.request.GET.get('phone'))
        if self.request.GET.get('city') and int(self.request.GET.get('city')) != 0:
            qs = qs.filter(city__id=int(self.request.GET.get('city')))
        if self.request.GET.get('type'):
            qs = qs.filter(type=int(self.request.GET.get('type')))
        return qs

    def get_context_data(self, **kwargs):
        context = super(TicketListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.type == 1:
            city_qs = City.objects.all()
        elif user.type == 2:
            city_qs = City.objects.filter(moderator=user)
        elif user.type == 5:
            manager = Manager.objects.get(user=user)
            city_qs = City.objects.filter(moderator=manager.moderator)
        else:
            city_qs = None
        context.update({
            'city_list': city_qs,
        })
        if self.request.GET.get('city'):
            context.update({
                'r_city': int(self.request.GET.get('city'))
            })
        if self.request.GET.get('type'):
            context.update({
                'r_type': int(self.request.GET.get('type'))
            })
        if self.request.GET.get('phone'):
            context.update({
                'r_phone': self.request.GET.get('phone')
            })
        if self.request.GET.get('name'):
            context.update({
                'r_name': self.request.GET.get('name')
            })
        return context


def ticket_detail(request, pk):
    context = {}
    user = request.user
    city_qs = City.objects.all()
    if user.type == 2:
        city_qs = city_qs.filter(moderator=user)
    elif user.type == 5:
        manager = Manager.objects.get(user=user)
        city_qs = city_qs.filter(moderator=manager.moderator)
    ticket = get_object_or_None(Ticket, pk=int(pk))
    if request.method == 'POST':
        form = TicketChangeForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('ticket:list'))
        else:
            context.update({
                'error': u'Проверьте правильность ввода данных'
            })
    else:
        form = TicketChangeForm(instance=ticket)
    form.fields['city'].queryset = city_qs
    context.update({
        'form': form,
        'object': ticket
    })
    return render(request, 'ticket/ticket_detail.html', context)
