# coding=utf-8
from datetime import datetime
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from apps.adjuster.models import SurfacePhoto
from apps.city.forms import CityAddForm, StreetForm, AreaAddForm, ManagementCompanyForm
from apps.city.models import City, Area, Street, ManagementCompany
from apps.client.models import ClientJournal
from apps.client.models import ClientJournalPayment
from apps.manager.models import Manager

__author__ = 'alexy'


class CityListView(ListView):
    model = City
    template_name = 'city/city_list.html'

    def get_queryset(self):
        user = self.request.user
        if user.type == 1:
            qs = City.objects.select_related('moderator').all()
        elif user.type == 2:
            qs = City.objects.select_related('moderator').filter(moderator=user)
        elif user.type == 6:
            qs = user.superviser.city.all()
        elif user.type == 5 and user.is_leader_manager():
            qs = City.objects.select_related('moderator').filter(moderator=user.manager.moderator)
        else:
            qs = None
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
    model = City
    form_class = CityAddForm
    template_name = 'city/city_add.html'


@login_required
def city_update(request, pk):
    user = request.user
    city = City.objects.get(pk=int(pk))
    if city.moderator == user or user.type == 1:
        # Если пользователь не является модератором города или администратором:
        # перенаправить его на страницу со списком своих городов
        pass
    else:
        if user.type == 5 and user.is_leader_manager():
            pass
        else:
            return HttpResponseRedirect(reverse('city:list'))

    if request.method == 'POST':
        form = CityAddForm(request.POST, instance=city)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(city.get_absolute_url())
    else:
        form = CityAddForm(instance=city)
        if user.type == 2:
            form.fields['name'].widget.attrs['readonly'] = True
            form.fields['moderator'].widget.attrs['readonly'] = True
        elif user.type == 5 and user.is_leader_manager():
            form.fields['name'].widget.attrs['readonly'] = True
            form.fields['moderator'].widget.attrs['readonly'] = True
    context = {
        'form': form,
        'city': city
    }
    return render(request, 'city/city_update.html', context)


@login_required
def city_area(request, pk):
    context = {}
    city = City.objects.get(pk=int(pk))
    if request.method == 'POST':
        form = AreaAddForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('city:area', args=(city.id, )))
        else:
            return HttpResponseRedirect(reverse('city:area', args=(city.id, )))
    else:
        form = AreaAddForm(
            initial={
                'city': city
            }
        )
    context.update({
        'city': city,
        'area_form': form
    })
    return render(request, 'city/city_area.html', context)


@login_required
def city_area_update(request, pk):
    context = {}
    area = Area.objects.get(pk=int(pk))
    if request.method == 'POST':
        form = AreaAddForm(request.POST, instance=area)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('city:area', args=(area.city.id, )))
        else:
            return HttpResponseRedirect(reverse('city:area-update', args=(area.id, )))
    else:
        form = AreaAddForm(instance=area)
    context.update({
        'city': area.city,
        'area': area,
        'area_form': form
    })
    return render(request, 'city/city_area_update.html', context)


@login_required
def city_street(request, pk):
    context = {}
    city = City.objects.get(pk=int(pk))
    if request.method == 'POST':
        form = StreetForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse('city:street', args=(city.id, )))
    else:
        form = StreetForm(
            initial={
                'city': city
            }
        )
        form.fields['area'].queryset = city.area_set.all()
    context.update({
        'city': city,
        'street_form': form
    })
    return render(request, 'city/city_street.html', context)


@login_required
def city_street_update(request, pk):
    context = {}
    street = Street.objects.get(pk=int(pk))
    if request.method == 'POST':
        form = StreetForm(request.POST, instance=street)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('city:street', args=(street.city.id, )))
        else:
            return HttpResponseRedirect(reverse('city:street-update', args=(street.id, )))
    else:
        form = StreetForm(instance=street)
        form.fields['area'].queryset = street.city.area_set.all()
    context.update({
        'city': street.city,
        'street': street,
        'street_form': form
    })
    return render(request, 'city/city_street_update.html', context)


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
