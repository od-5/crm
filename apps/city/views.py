# coding=utf-8
from django.core.urlresolvers import reverse
from django.forms import inlineformset_factory, TextInput
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from apps.city.forms import CityAddForm, SurfaceAddForm, PorchFormSet
from apps.city.models import City, Area, Surface

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
    context = {
        'form': form,
        'formset': formset,
    }
    return render(request, 'city/city_form.html', context)


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
        print user_id
        if self.request.user.type == 1:
            qs = Surface.objects.all()
        elif self.request.user.type == 2:
            qs = Surface.objects.filter(city__moderator=user_id)
        else:
            qs = None
        queryset = qs
        return queryset

    # def get_context_data(self, **kwargs):
    #     context = super(ExcurseListView, self).get_context_data(**kwargs)
    #     qs = Excurse.objects.all()
    #     context.update(
    #         qs.aggregate(Min('price'))
    #     )
    #     context.update(
    #         qs.aggregate(Max('price'))
    #     )
    #     context.update({
    #         'excurse_section_list': ExcurseSection.objects.all()
    #     })
    #     return context


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
    return HttpResponseRedirect('/city/')
