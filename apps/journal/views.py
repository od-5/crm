# coding=utf-8
from datetime import datetime
from django.db.models import Sum
from django.views.generic import ListView

from apps.city.mixin import CityListMixin
from apps.city.models import City
from apps.client.models import ClientJournal, ClientJournalPayment
from apps.manager.mixin import ManagerListMixin
from apps.manager.models import Manager

__author__ = 'alexy'


class JournalListView(ListView, CityListMixin, ManagerListMixin):
    model = ClientJournal
    template_name = 'journal/journal_list.html'
    paginate_by = 50

    def get_queryset(self):
        user = self.request.user
        qs = self.model.objects.get_qs(user).prefetch_related('client', 'client__manager', 'clientorder')
        if self.request.GET.get('city'):
            qs = qs.filter(client__city=int(self.request.GET.get('city')))
        if self.request.GET.get('legal_name'):
            qs = qs.filter(client__legal_name__icontains=self.request.GET.get('legal_name'))
        if self.request.GET.get('manager'):
            qs = qs.filter(client__manager=self.request.GET.get('manager'))
        if self.request.GET.get('date_s'):
            qs = qs.filter(created__gte=datetime.strptime(self.request.GET.get('date_s'), '%d.%m.%Y'))
        if self.request.GET.get('date_e'):
            qs = qs.filter(created__lte=datetime.strptime(self.request.GET.get('date_e'), '%d.%m.%Y'))
        if self.request.GET.get('payment'):
            payment = int(self.request.GET.get('payment'))
            if payment == 0:
                qs = qs.filter(has_payment=False)
            elif payment == 1:
                qs = qs.filter(full_payment=True)
            elif payment == 2:
                qs = qs.filter(full_payment=False, has_payment=True)
            elif payment == 3:
                qs = qs.filter(has_payment=True)
        return qs

    def get_context_data(self, **kwargs):
        context = super(JournalListView, self).get_context_data(**kwargs)
        r_city = self.request.GET.get('city')
        r_manager = self.request.GET.get('manager')
        if self.request.GET.get('payment'):
            context.update({
                'r_payment': int(self.request.GET.get('payment'))
            })
        if self.request.GET.get('date_s'):
            context.update({
                'r_date_s': self.request.GET.get('date_s')
            })
        if self.request.GET.get('date_e'):
            context.update({
                'r_date_e': self.request.GET.get('date_e')
            })
        if self.request.GET.get('legal_name'):
            context.update({
                'r_legal_name': self.request.GET.get('legal_name')
            })
        if r_manager:
            context.update({
                'r_manager': int(r_manager)
            })
        try:
            total_cost = self.object_list.aggregate(Sum('full_cost'))['full_cost__sum']
        except:
            total_cost = 0
        try:
            payments_sum = self.object_list.aggregate(Sum('total_payment'))['total_payment__sum']
        except:
            payments_sum = 0
        if not r_city:
            r_city = 0
        context.update({
            'r_city': int(r_city),
            'total_cost': total_cost,
            'payments_sum': payments_sum
        })
        return context


class ClientJournalPaymentListView(ListView, CityListMixin, ManagerListMixin):
    model = ClientJournalPayment
    template_name = 'journal/cientjournalpayment_list.html'
    paginate_by = 50

    def get_queryset(self):
        user = self.request.user
        qs = self.model.objects.get_qs(user).select_related('client', 'client__manager__user', 'clientjournal')
        city = self.request.GET.get('city')
        date_s = self.request.GET.get('date_s')
        date_e = self.request.GET.get('date_e')
        legal_name = self.request.GET.get('legal_name')
        manager = self.request.GET.get('manager')
        if city and city != 0:
            qs = qs.filter(client__city=int(city))
        if legal_name:
            qs = qs.filter(client__legal_name__icontains=legal_name)
        if manager:
            qs = qs.filter(client__manager=manager)
        if date_s:
            qs = qs.filter(created__gte=datetime.strptime(date_s, '%d.%m.%Y'))
        if date_e:
            qs = qs.filter(created__lte=datetime.strptime(date_e, '%d.%m.%Y'))
        return qs

    def get_context_data(self, **kwargs):
        context = super(ClientJournalPaymentListView, self).get_context_data(**kwargs)
        if self.request.GET.get('city') and int(self.request.GET.get('city')) != 0:
            context.update({
                'r_city': int(self.request.GET.get('city'))
            })
        if self.request.GET.get('manager') and int(self.request.GET.get('manager')) != 0:
            context.update({
                'r_manager': int(self.request.GET.get('manager'))
            })
        if self.request.GET.get('date_s'):
            context.update({
                'r_date_s': self.request.GET.get('date_s')
            })
        if self.request.GET.get('date_e'):
            context.update({
                'r_date_e': self.request.GET.get('date_e')
            })
        if self.request.GET.get('legal_name'):
            context.update({
                'r_legal_name': self.request.GET.get('legal_name')
            })
        payments_sum = 0
        for i in self.object_list:
            payments_sum += float(i.sum)
        context.update({
            'payments_sum': round(payments_sum, 2)
        })
        return context

