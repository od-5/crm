# coding=utf-8
from datetime import datetime
from django.views.generic import ListView
from apps.city.models import City
from apps.client.models import ClientJournal
from apps.manager.models import Manager

__author__ = 'alexy'


class JournalListView(ListView):
    model = ClientJournal
    template_name = 'journal/journal_list.html'
    paginate_by = 50

    def get_queryset(self):
        user = self.request.user
        if self.request.user.type == 1:
            qs = ClientJournal.objects.all()
        elif self.request.user.type == 2:
            qs = ClientJournal.objects.filter(client__city__moderator=user)
        elif self.request.user.type == 5:
            qs = ClientJournal.objects.filter(client__manager=user)
        else:
            qs = None
        if self.request.GET.get('city'):
            qs = qs.filter(client__city=int(self.request.GET.get('city')))
        if self.request.GET.get('legal_name'):
            qs = qs.filter(client__legal_name__iexact=self.request.GET.get('legal_name'))
        if self.request.GET.get('manager'):
            qs = qs.filter(client__manager=self.request.GET.get('manager'))
        if self.request.GET.get('date_s'):
            qs = qs.filter(created__gte=datetime.strptime(self.request.GET.get('date_s'), '%d.%m.%Y'))
        if self.request.GET.get('date_e'):
            qs = qs.filter(created__lte=datetime.strptime(self.request.GET.get('date_e'), '%d.%m.%Y'))
        return qs

    def get_context_data(self, **kwargs):
        context = super(JournalListView, self).get_context_data(**kwargs)
        user = self.request.user
        if self.request.user.type == 1:
            city_qs = City.objects.all()
            manager_qs = Manager.objects.all()
        elif self.request.user.type == 2:
            city_qs = City.objects.filter(moderator=user)
            manager_qs = Manager.objects.filter(moderator=user)
        elif self.request.user.type == 5:
            current_manager = Manager.objects.get(user=user)
            city_qs = City.objects.filter(moderator=current_manager.moderator)
            manager_qs = Manager.objects.filter(moderator=current_manager.moderator)
        else:
            city_qs = None
            manager_qs = None
        r_city = self.request.GET.get('city')
        r_manager = self.request.GET.get('manager')
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
        total_cost = 0
        for i in self.object_list:
            total_cost += i.total_cost()
        if not r_city:
            r_city = 0
        context.update({
            'city_list': city_qs,
            'manager_list': manager_qs,
            'r_city': int(r_city),
            'total_cost': total_cost
        })
        return context
