# coding=utf-8
from datetime import datetime
from django.db.models import Sum
from django.views.generic import ListView
from apps.city.models import City
from apps.client.models import ClientJournal, ClientJournalPayment
from apps.manager.models import Manager

__author__ = 'alexy'


class JournalListView(ListView):
    model = ClientJournal
    template_name = 'journal/journal_list.html'
    paginate_by = 50

    def get_queryset(self):
        user = self.request.user
        if user.type == 1:
            qs = ClientJournal.objects.prefetch_related('client', 'client__manager', 'clientorder').all()
        elif user.type == 6:
            qs = ClientJournal.objects.prefetch_related('client', 'client__manager', 'clientorder').filter(
                client__city__in=user.superviser.city_id_list())
        elif user.type == 2:
            qs = ClientJournal.objects.prefetch_related('client', 'client__manager', 'clientorder').filter(
                client__city__moderator=user)
        elif user.type == 5:
            if user.is_leader_manager():
                qs = ClientJournal.objects.prefetch_related('client', 'client__manager', 'clientorder').filter(
                    client__city__moderator=user.manager.moderator)
            else:
                qs = ClientJournal.objects.prefetch_related('client', 'client__manager', 'clientorder').filter(
                    client__manager=user.manager)
        else:
            qs = None
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
        user = self.request.user
        if user.type == 1:
            city_qs = City.objects.all()
            manager_qs = Manager.objects.select_related('user').all()
        elif user.type == 6:
            city_qs = user.superviser.city.all()
            manager_qs = Manager.objects.select_related('user').filter(moderator__in=user.superviser.moderator_id_list())
        elif self.request.user.type == 2:
            city_qs = City.objects.filter(moderator=user)
            manager_qs = Manager.objects.select_related('user').filter(moderator=user)
        elif self.request.user.type == 5:
            manager = Manager.objects.get(user=user)
            city_qs = City.objects.filter(moderator=manager.moderator)
            manager_qs = Manager.objects.select_related('user').filter(moderator=manager.moderator)
        else:
            city_qs = None
            manager_qs = None
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
        # for i in self.object_list:
        #     total_cost += i.total_cost()
        #     payments_sum += i.current_payment()
        if not r_city:
            r_city = 0
        context.update({
            'city_list': city_qs,
            'manager_list': manager_qs,
            'r_city': int(r_city),
            'total_cost': total_cost,
            'payments_sum': payments_sum
        })
        return context


class ClientJournalPaymentListView(ListView):
    model = ClientJournalPayment
    template_name = 'journal/cientjournalpayment_list.html'
    paginate_by = 50

    def get_queryset(self):
        user = self.request.user
        if user.type == 1:
            qs = ClientJournalPayment.objects.select_related('client', 'client__manager__user', 'clientjournal').all()
        elif user.type == 6:
            qs = ClientJournalPayment.objects.select_related(
                'client', 'client__manager__user', 'clientjournal').filter(
                client__city__in=user.superviser.city_id_list())
        elif user.type == 2:
            qs = ClientJournalPayment.objects.select_related(
                'client', 'client__manager__user', 'clientjournal').filter(
                client__manager__moderator=user)
        elif user.type == 5:
            if user.is_leader_manager():
                qs = ClientJournalPayment.objects.select_related(
                    'client', 'client__manager__user', 'clientjournal').filter(
                    client__city__moderator=user.manager.moderator)
            else:
                qs = ClientJournalPayment.objects.select_related(
                    'client', 'client__manager__user', 'clientjournal').filter(
                    client__manager=user.manager)
        else:
            qs = None
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
        user = self.request.user
        if self.request.user.type == 1:
            city_qs = City.objects.all()
            manager_qs = Manager.objects.select_related('user').all()
        elif self.request.user.type == 6:
            city_qs = user.superviser.city.all()
            manager_qs = Manager.objects.select_related('user').filter(
                moderator__in=user.superviser.moderator_id_list())
        elif self.request.user.type == 2:
            city_qs = City.objects.filter(moderator=user)
            manager_qs = Manager.objects.select_related('user').filter(moderator=user)
        elif self.request.user.type == 5:
            city_qs = City.objects.filter(moderator=user.manager.moderator)
            manager_qs = Manager.objects.select_related('user').filter(moderator=user.manager.moderator)
        else:
            city_qs = None
            manager_qs = None
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
            'city_list': city_qs,
            'manager_list': manager_qs,
            'payments_sum': round(payments_sum, 2)
        })
        return context

