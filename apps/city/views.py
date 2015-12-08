# coding=utf-8
from django.forms import inlineformset_factory, TextInput
from django.http import HttpResponseRedirect
from django.shortcuts import render
from apps.city.forms import CityAddForm
from apps.city.models import City, Area

__author__ = 'alexy'


def city_update(request, pk):
    city = City.objects.get(pk=int(pk))
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