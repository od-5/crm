# coding=utf-8
from datetime import datetime
from django.core.urlresolvers import reverse
from django.forms import inlineformset_factory, TextInput, Select, formset_factory, modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.dateparse import parse_date, parse_time
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from apps.adjuster.models import SurfacePhoto
from apps.city.forms import CityAddForm, StreetForm, AreaAddForm, AreaModelFormset
from apps.city.models import City, Area, Surface, Street

__author__ = 'alexy'


class CityListView(ListView):
    model = City

    def get_queryset(self):
        user_id = self.request.user.id
        if self.request.user.type == 1:
            qs = City.objects.all()
        elif self.request.user.type == 2:
            qs = City.objects.filter(moderator=user_id)
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
        if self.request.user.type == 1:
            qs = City.objects.all()
        elif self.request.user.type == 2:
            qs = City.objects.filter(moderator=self.request.user.id)
        else:
            qs = None
        context.update({
            'user_city_list': qs
        })
        if self.request.user.type == 1:
            a_qs = SurfacePhoto.objects.all()
        elif self.request.user.type == 2:
            a_qs = SurfacePhoto.objects.select_related('moderator').filter(pk=int(self.request.user.id))
        else:
            a_qs = None
        if a_qs:
            if self.request.GET.get('broken'):
                context.update({
                    'show_broken': True
                })
                a_qs = a_qs.filter(is_broken=True)
            else:
                a_qs = a_qs.filter(is_broken=False)
            if self.request.GET.get('start_date'):
                context.update({
                    'start_date': self.request.GET.get('start_date')
                })
                start_date = self.request.GET.get('start_date')
                rs_date = datetime.strptime(start_date, '%d.%m.%Y')
                s_date = datetime.date(rs_date)
                # c_surface.date_start = datetime.date(raw_date.year, raw_date.month, raw_date.day)
                a_qs = a_qs.filter(date__gte=s_date)
                # print s_date
                if self.request.GET.get('end_date'):
                    print self.request.GET.get('end_date')
                    end_date = self.request.GET.get('end_date')
                    re_date = datetime.strptime(end_date, '%d.%m.%Y')
                    e_date = datetime.date(re_date)
                    # c_surface.date_start = datetime.date(raw_date.year, raw_date.month, raw_date.day)
                    a_qs = a_qs.filter(date__lte=e_date)
                    context.update({
                        'end_date': self.request.GET.get('end_date')
                    })
        if self.request.GET.get('grid') and int(self.request.GET.get('grid')) == 1:
            context.update({
                'grid': True
            })
        paginator = Paginator(a_qs, 20) # Show 25 contacts per page
        page = self.request.GET.get('page')
        try:
            address_list = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            address_list = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            address_list = paginator.page(paginator.num_pages)
        context.update({
            'address_list': address_list
        })

        return context


class CityCreateView(CreateView):
    model = City
    form_class = CityAddForm
    template_name = 'city/city_add.html'


def city_update(request, pk):
    user = request.user
    city = City.objects.get(pk=int(pk))
    if city.moderator == user or user.type == 1:
        # Если пользователь не является модератором города или администратором:
        # перенаправить его на страницу со списком своих городов
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
    context = {
        'form': form,
        'city': city
    }
    return render(request, 'city/city_update.html', context)


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


def city_street_update(request, pk):
    context = {}
    street = Street.objects.get(pk=int(pk))
    City
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
