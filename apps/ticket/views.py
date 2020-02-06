# coding=utf-8
from annoying.functions import get_object_or_None
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import ListView, UpdateView, CreateView
from apps.city.models import City
from apps.manager.models import Manager
from apps.ticket.forms import TicketChangeForm
from .models import Ticket

__author__ = 'alexy'


class TicketListView(ListView):
    model = Ticket
    paginate_by = 25
    template_name = 'ticket/ticket_list.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TicketListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if user.type == 1:
            qs = Ticket.objects.all()
        elif user.type == 6:
            qs = Ticket.objects.filter(city__in=user.superviser.city_id_list())
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
        city_qs = City.objects.get_qs(user)
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


class TicketView(CreateView):
    model = Ticket
    fields = ('name', 'phone', 'city', 'email')
    success_url = reverse_lazy('ok')

    def form_invalid(self, form):
        return HttpResponseRedirect(reverse_lazy('no-ok'))


class TicketUpdateView(UpdateView):
    model = Ticket
    form_class = TicketChangeForm
    template_name = 'ticket/ticket_detail.html'
    success_url = reverse_lazy('ticket:list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TicketUpdateView, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(TicketUpdateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


@login_required
def ticket_detail(request, pk):
    context = {}
    user = request.user
    # if user.type == 1:
    #     city_qs = City.objects.all()
    # elif user.type == 6:
    #     city_qs = user.superviser.city.all()
    # elif user.type == 2:
    #     city_qs = City.objects.filter(moderator=user)
    # elif user.type == 5:
    #     # manager = Manager.objects.get(user=user)
    #     city_qs = City.objects.filter(moderator=user.manager.moderator)
    # else:
    #     city_qs = None
    ticket = get_object_or_None(Ticket, pk=int(pk))
    if request.method == 'POST':
        form = TicketChangeForm(request.POST, user=user, instance=ticket)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('ticket:list'))
        else:
            context.update({
                'error': u'Проверьте правильность ввода данных'
            })
    else:
        form = TicketChangeForm(instance=ticket, user=user)
    # form.fields['city'].queryset = city_qs
    context.update({
        'form': form,
        'object': ticket
    })
    return render(request, 'ticket/ticket_detail.html', context)
