# coding=utf-8
from datetime import datetime
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Sum, Count
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from apps.adjuster.models import SurfacePhoto
from apps.city.forms import CityForm, StreetForm, AreaForm, ManagementCompanyForm
from apps.city.models import City, Area, Street, ManagementCompany
from apps.client.models import ClientJournal
from apps.client.models import ClientJournalPayment
from apps.manager.models import Manager

__author__ = 'alexy'


class CityListView(ListView):
    """
    Список городов
    """

    model = City
    template_name = 'city/city_list.html'

    def get_queryset(self):
        user = self.request.user
        qs = self.model.objects.get_qs(user).select_related('moderator').annotate(
            num_porch=Count('surface__porch'), num_client=Count('client'))
        if self.request.GET.get('moderator'):
            qs = qs.filter(moderator__email=self.request.GET.get('moderator'))
        if self.request.GET.get('city') and int(self.request.GET.get('city')) != 0:
            qs = qs.filter(id=int(self.request.GET.get('city')))
        return qs

    @csrf_exempt
    def get_context_data(self, **kwargs):
        context = super(CityListView, self).get_context_data()
        if self.request.GET.get('city') and int(self.request.GET.get('city')) != 0:
            context.update({
                'city_id': int(self.request.GET.get('city'))
            })
        context.update({
            'user_city_list': self.object_list
        })
        return context


class CityCreateView(CreateView):
    """
    Создание города
    """
    model = City
    form_class = CityForm
    template_name = 'city/city_add.html'


class CityUpdateView(UpdateView):
    """
    Реактирование города
    """
    model = City
    form_class = CityForm
    template_name = 'city/city_update.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        city = self.get_object()
        if user.type == 1 or city.moderator == user or \
                user.type == 5 and user.is_leader_manager() and city.moderator == user.manager.moderator:
            return super(CityUpdateView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse_lazy('city:list'))

    def get_form_kwargs(self):
        kwargs = super(CityUpdateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        if self.request.user == 1:
            return super(CityUpdateView, self).form_valid(form)
        else:
            return HttpResponseRedirect(self.object.get_absolute_url())

    def form_invalid(self, form):
        if self.request.user == 1:
            return super(CityUpdateView, self).form_invalid(form)
        else:
            return HttpResponseRedirect(self.object.get_absolute_url())


class AreaAddView(CreateView):
    model = Area
    form_class = AreaForm
    template_name = 'city/city_area.html'

    def get_city(self):
        if 'pk' in self.kwargs:
            city = City.objects.get(pk=self.kwargs['pk'])
            return city
        else:
            raise Http404

    def get_initial(self):
        return {
            'city': self.get_city()
        }

    def get_context_data(self, **kwargs):
        context = super(AreaAddView, self).get_context_data(**kwargs)
        city = self.get_city()
        context.update({
            'city': city,
            'area_list': city.area_set.annotate(num_street=Count('street'))
        })
        return context


class AreaUpdateView(UpdateView):
    model = Area
    form_class = AreaForm
    template_name = 'city/city_area_update.html'

    def get_city(self):
        if 'pk' in self.kwargs:
            city = City.objects.get(pk=self.kwargs['pk'])
            return city
        else:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super(AreaUpdateView, self).get_context_data(**kwargs)
        context.update({
            'city': self.object.city
        })
        return context


class StreetAddView(CreateView):
    model = Street
    form_class = StreetForm
    template_name = 'city/city_street.html'

    def get_city(self):
        if 'pk' in self.kwargs:
            city = City.objects.get(pk=self.kwargs['pk'])
            return city
        else:
            raise Http404

    def get_initial(self):
        return {
            'city': self.get_city()
        }

    def get_context_data(self, **kwargs):
        context = super(StreetAddView, self).get_context_data(**kwargs)
        city = self.get_city()
        context.update({
            'city': city,
        })
        return context


class StreetUpdateView(UpdateView):
    model = Street
    form_class = StreetForm
    template_name = 'city/city_street_update.html'


@login_required
def management_company_list(request):
    context = {}
    if request.user.type == 1:
        qs = ManagementCompany.objects.all()
        city_qs = City.objects.all()
    elif request.user.type == 6:
        qs = ManagementCompany.objects.filter(city__in=request.user.superviser.city_id_list())
        city_qs = request.user.superviser.city.all()
    elif request.user.type == 2:
        qs = ManagementCompany.objects.filter(city__moderator=request.user)
        city_qs = City.objects.filter(moderator=request.user)
    else:
        qs = None
        city_qs = None
    if request.GET.get('city') and int(request.GET.get('city')) != 0:
        qs = qs.filter(city=int(request.GET.get('city')))
        context.update({
            'city_id': int(request.GET.get('city'))
        })
    if request.GET.get('name'):
        qs = qs.filter(name__icontains=request.GET.get('name'))
    if request.META['QUERY_STRING']:
        request.session['mc_filtered_list'] = '%s?%s' % (request.path, request.META['QUERY_STRING'])
    else:
        request.session['mc_filtered_list'] = reverse('city:management-company')
    context.update({
        'object_list': qs,
        'city_list': city_qs
    })
    return render(request, 'city/management_company_list.html', context)


@login_required
def management_company_add(request):
    context = {}
    if request.method == 'POST':
        form = ManagementCompanyForm(request.POST, request=request)
        if form.is_valid():
            management_company = form.save()
            return HttpResponseRedirect(reverse('city:management-company-update', args=(management_company.id, )))
    else:
        form = ManagementCompanyForm(request=request)
    try:
        request.session['mc_filtered_list']
    except:
        request.session['mc_filtered_list'] = reverse('city:management-company')
    context.update({
        'form': form,
        'back_to_list': request.session['mc_filtered_list']
    })
    return render(request, 'city/management_company.html', context)


@login_required
def management_company_update(request, pk):
    context = {}
    m_company = ManagementCompany.objects.get(pk=int(pk))
    if request.method == 'POST':
        form = ManagementCompanyForm(request.POST, request=request, instance=m_company)
        if form.is_valid():
            form.save()
    else:
        form = ManagementCompanyForm(request=request, instance=m_company)
    try:
        request.session['mc_filtered_list']
    except:
        request.session['mc_filtered_list'] = reverse('city:management-company')
    context.update({
        'form': form,
        'object': m_company,
        'back_to_list': request.session['mc_filtered_list']
    })
    return render(request, 'city/management_company.html', context)


@login_required
def city_report(request):
    context = {}
    user = request.user
    total_cost = total_payment = 0
    if user.type == 1:
        city_qs = City.objects.select_related().all()
    elif user.type == 6:
        city_qs = user.superviser.city.all()
    elif user.type == 2:
        city_qs = City.objects.select_related().filter(moderator=user)
    elif user.type == 5 and user.is_leader_manager():
        city_qs = City.objects.select_related().filter(moderator=user.manager.moderator)
    else:
        city_qs = None
    r_city = request.GET.get('city')
    r_date_s = request.GET.get('date_s')
    r_date_e = request.GET.get('date_e')
    if r_date_s:
        context.update({
            'r_date_s': r_date_s
        })
    if r_date_e:
        context.update({
            'r_date_e': r_date_e
        })
    for city_item in city_qs:
        city_journal_qs = ClientJournal.objects.filter(client__city=city_item)
        # city_payment_qs = ClientJournalPayment.objects.filter(client__city=city_item)
        if r_date_s:
            city_journal_qs = city_journal_qs.filter(created__gte=datetime.strptime(r_date_s, '%d.%m.%Y'))
            # city_payment_qs = city_payment_qs.filter(created__gte=datetime.strptime(r_date_s, '%d.%m.%Y'))
        if r_date_e:
            city_journal_qs = city_journal_qs.filter(created__gte=datetime.strptime(r_date_s, '%d.%m.%Y'))
            # city_payment_qs = city_payment_qs.filter(created__gte=datetime.strptime(r_date_s, '%d.%m.%Y'))
        city_item.total_cost = 0
        # city_total_payment = city_payment_qs.aggregate(Sum('sum'))
        # city_item.total_payment = city_total_payment['sum__sum']
        for item in city_journal_qs:
            city_item.total_cost += item.total_cost()
    if r_city and int(r_city) != 0:
        city = city_qs.get(id=int(r_city))
        journal_qs = ClientJournal.objects.filter(client__city=city)
        payment_qs = ClientJournalPayment.objects.filter(client__city=city)
        if r_date_s:
            journal_qs = journal_qs.filter(created__gte=datetime.strptime(r_date_s, '%d.%m.%Y'))
            payment_qs = payment_qs.filter(created__gte=datetime.strptime(r_date_s, '%d.%m.%Y'))
        if r_date_e:
            journal_qs = journal_qs.filter(created__gte=datetime.strptime(r_date_s, '%d.%m.%Y'))
            payment_qs = payment_qs.filter(created__gte=datetime.strptime(r_date_s, '%d.%m.%Y'))

        total_payment = payment_qs.aggregate(Sum('sum'))['sum__sum']
        for item in journal_qs:
            total_cost += item.total_cost()
    else:
        city = None
    context.update({
        'city_list': city_qs,
        'city': city,
        'total_payment': total_payment,
        'total_cost': total_cost
    })
    return render(request, 'city/city_report.html', context)
