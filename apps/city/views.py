# coding=utf-8
from django.core.urlresolvers import reverse
from django.forms import inlineformset_factory, TextInput, Select, formset_factory, modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from apps.city.forms import CityAddForm, SurfaceAddForm, PorchFormSet, StreetForm
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
            print '*2'*10
            formset.save()
            return HttpResponseRedirect(city.get_absolute_url())
        else:
            print u'Форма не валидна!!!!!!!!!!!!!!!!!!!!'

    else:
        print 'METHOD != POST'
        form = CityAddForm(instance=city)
        formset = AreaInlineFormset(instance=city)
        street_form = StreetForm(
            initial={
                'city': city,
                # 'area': city.area_set.all(),
                'name': u'Привет'
            }
        )
    context = {
        'form': form,
        'formset': formset,
        'street_form': street_form,
        'city': city
    }
    return render(request, 'city/city_form.html', context)


def street_add(request):
    if request.method == 'POST':
        form = StreetForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return HttpResponseRedirect(reverse('city:list'))
    else:
        return HttpResponseRedirect(reverse('city:list'))


class CityListView(ListView):
    model = City

    def get_queryset(self):
        user_id = self.request.user.id
        print user_id
        if self.request.user.type == 1:
            qs = City.objects.all()
        elif self.request.user.type == 2:
            qs = City.objects.filter(moderator=user_id)
        else:
            qs = None
        queryset = qs
        return queryset


class SurfaceListView(ListView):
    model = Surface

    def get_queryset(self):
        user_id = self.request.user.id
        if self.request.user.type == 1:
            qs = Surface.objects.all()
            print 'admin'
            print qs
        elif self.request.user.type == 2:
            qs = Surface.objects.filter(city__moderator=user_id)
            print 'moderator'
            print qs
        else:
            print 'None'
            qs = None
            print qs
        if self.request.GET.get('city') and int(self.request.GET.get('city')) != 0:
            queryset = qs.filter(city__id=int(self.request.GET.get('city')))
            if self.request.GET.get('area') and int(self.request.GET.get('area')) != 0:
                queryset = queryset.filter(street__area__id=int(self.request.GET.get('area')))
                if self.request.GET.get('street') and int(self.request.GET.get('street')) != 0:
                    queryset = queryset.filter(street__id=int(self.request.GET.get('street')))
        else:
            queryset = qs
        print queryset
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
        porch_form = PorchFormSet(instance=self.object)
        # print porch_form
        context.update({
            'porch_form': porch_form
        })
        return context


def porch_update(request):
    if request.method == 'POST':
        surface_id = request.POST.get('surface_id')
        surface = Surface.objects.get(pk=int(surface_id))
        formset = PorchFormSet(request.POST, instance=surface)
        if formset.is_valid():
            formset.save()
        else:
            print u'Формсет валиден'
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
