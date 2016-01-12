# coding=utf-8
from datetime import datetime
from django.core.urlresolvers import reverse
from django.forms import inlineformset_factory, TextInput, Select, formset_factory, modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.dateparse import parse_date, parse_time
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView
from apps.adjuster.models import SurfacePhoto
from apps.city.forms import CityAddForm, SurfaceAddForm, PorchFormSet, StreetForm, SurfacePhotoAddForm, \
    SurfaceClientAddForm, AreaAddForm, AreaModelFormset
from apps.city.models import City, Area, Surface, Street

__author__ = 'alexy'


def city_update(request, pk):
    user = request.user
    city = City.objects.get(pk=int(pk))

    if city.moderator == user or user.type == 1:
        # Если пользователь не является модератором города или администратором:
        # перенаправить его на страницу со списком своих городов
        pass
    else:
        return HttpResponseRedirect(reverse('city:list'))

    AreaInlineFormset = inlineformset_factory(
        City,
        Area,
        fields=('name',),
        widgets={
            'name': TextInput(attrs={'class': 'form-control'}),
        },
        extra=2
    )

    if request.method == 'POST':
        form = CityAddForm(request.POST, instance=city)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(city.get_absolute_url())

        formset = AreaInlineFormset(request.POST, request.FILES, instance=city)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(city.get_absolute_url())
    else:
        form = CityAddForm(instance=city)
        if user.type == 2:
            form.fields['name'].widget.attrs['readonly'] = True
            form.fields['moderator'].widget.attrs['readonly'] = True
        formset = AreaInlineFormset(instance=city)
    street_form = StreetForm(
        initial={
            'city': city
        }
    )
    street_form.fields['area'].queryset = city.area_set.all()
    area_form = AreaAddForm(initial={
        'city': city
    })
    context = {
        'form': form,
        'formset': formset,
        'street_form': street_form,
        'city': city,
        'area_form': area_form
    }
    return render(request, 'city/city_form.html', context)


def area_add(request):
    if request.method == 'POST':
        formset = AreaModelFormset(request.POST)
        print formset
        if formset.is_valid():
            print 'Valid'
            instanes = formset.save(commit=False)
            for instance in instanes:
                instance.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            print 'Not Valid'


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
            queryset = qs.filter(moderator__email=self.request.GET.get('moderator'))
        else:
            if self.request.GET.get('city') and int(self.request.GET.get('city')) != 0:
                queryset = qs.filter(id=int(self.request.GET.get('city')))
            else:
                queryset = qs
        return queryset

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
            # TODO: сделать queryset для модератора, только по его городам
            a_qs = SurfacePhoto.objects.all()
        elif self.request.user.type == 2:
            a_qs = SurfacePhoto.objects.select_related('moderator').filter(pk=int(self.request.user.id))
        else:
            a_qs = None
        if a_qs:
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
        context.update({
            'address_list': a_qs
        })

        return context


class SurfaceListView(ListView):
    model = Surface

    def get_queryset(self):
        user_id = self.request.user.id
        if self.request.user.type == 1:
            qs = Surface.objects.all()
        elif self.request.user.type == 2:
            qs = Surface.objects.filter(city__moderator=user_id)
        else:
            qs = None
        if self.request.GET.get('city') and int(self.request.GET.get('city')) != 0:
            queryset = qs.filter(city__id=int(self.request.GET.get('city')))
            if self.request.GET.get('area') and int(self.request.GET.get('area')) != 0:
                queryset = queryset.filter(street__area__id=int(self.request.GET.get('area')))
                if self.request.GET.get('street') and int(self.request.GET.get('street')) != 0:
                    queryset = queryset.filter(street__id=int(self.request.GET.get('street')))
        else:
            queryset = qs
        return queryset

    def get_context_data(self, **kwargs):
        context = super(SurfaceListView, self).get_context_data(**kwargs)
        user_id = self.request.user.id
        if self.request.user.type == 1:
            qs = City.objects.all()
        elif self.request.user.type == 2:
            qs = City.objects.filter(moderator=user_id)
        else:
            qs = None
        context.update({
            'city_list': qs
        })
        if self.request.GET.get('city'):
            area_qs = Area.objects.filter(city__id=int(self.request.GET.get('city')))
            context.update({
                'area_list': area_qs,
                'city_id': int(self.request.GET.get('city'))
            })
            if self.request.GET.get('area'):
                street_qs = Street.objects.filter(area__id=int(self.request.GET.get('area')))
                context.update({
                    'street_list': street_qs,
                    'area_id': int(self.request.GET.get('area'))
                })
                if self.request.GET.get('street'):
                    context.update({
                        'street_id': int(self.request.GET.get('street'))
                    })
                    # if self.request.GET.get('street'):
                    #     house_number_qs = Surface.objects.filter(area=int(self.request.GET.get('area')))
                    #     context.update({
                    #         'street_list': street_qs,
                    #         'area_id': int(self.request.GET.get('area'))
                    #     })

        return context


class SurfaceCreateView(CreateView):
    model = Surface
    form_class = SurfaceAddForm
    template_name = 'city/surface_add.html'

    def get_initial(self):
        """
        Добавление request.user в форму, для ограничения
        в зависимости от уровня доступа пользователя
        """
        initial = super(SurfaceCreateView, self).get_initial()
        user = self.request.user
        initial = initial.copy()
        initial['user'] = self.request.user
        return initial


class SurfaceUpdateView(UpdateView):
    model = Surface
    template_name = 'city/surface_form.html'
    form_class = SurfaceAddForm

    # def get_object(self, queryset=None):
    #     print self.request.user
    #     return self.request.user

    def get_initial(self):
        """
        Добавление request.user в форму, для ограничения
        в зависимости от уровня доступа пользователя
        """
        initial = super(SurfaceUpdateView, self).get_initial()
        user = self.request.user
        initial = initial.copy()
        initial['user'] = self.request.user
        return initial

    def get_context_data(self, **kwargs):
        context = super(SurfaceUpdateView, self).get_context_data(**kwargs)
        # print self.object
        surface_photo_form = SurfacePhotoAddForm(
            initial={
                'surface': self.object
            }
        )
        surface_photo_form.fields['porch'].queryset = self.object.porch_set.all()
        porch_form = PorchFormSet(instance=self.object)
        surface_client_form = SurfaceClientAddForm(
            initial={
                'surface': self.object
            }
        )
        surface_client_form.fields['client'].queryset = self.object.city.client_set.all()

        context.update({
            'porch_form': porch_form,
            'surface_photo_form': surface_photo_form,
            'surface_client_form': surface_client_form
        })
        return context


def porch_update(request):
    if request.method == 'POST':
        surface_id = request.POST.get('surface_id')
        surface = Surface.objects.get(pk=int(surface_id))
        formset = PorchFormSet(request.POST, instance=surface)
        if formset.is_valid():
            formset.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def surface_photo_add(request):
    if request.method == 'POST':
        form = SurfacePhotoAddForm(request.POST, request.FILES)
        if form.is_valid():
            # file is saved
            form.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def add_surface_client(request):
    if request.method == 'POST':
        form = SurfaceClientAddForm(request.POST)
        if form.is_valid():
            # file is saved
            form.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
