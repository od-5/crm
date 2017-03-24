# coding=utf-8
from annoying.functions import get_object_or_None
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView
from apps.city.models import City
from .forms import SetupForm, BlockEffectiveForm, BlockExampleForm, BlockReviewForm
from .models import Setup, BlockEffective, BlockReview, BlockExample

__author__ = 'alexy'


class LandingView(TemplateView):
    template_name = 'landing/index.html'

    def get_context_data(self, **kwargs):
        context = {}
        city_qs = City.objects.values('id', 'name')
        # city_qs = City.objects.all()
        current_city = get_object_or_None(City, slug=self.request.subdomain)
        if current_city:
            try:
                setup = Setup.objects.get(city=current_city)
            except:
                setup = Setup.objects.filter(city__isnull=True).first()
            blockeffective_qs = BlockEffective.objects.filter(city=current_city)
            if not blockeffective_qs:
                blockeffective_qs = BlockEffective.objects.filter(city__isnull=True)
            blockreview_qs = BlockReview.objects.filter(city=current_city)
            if not blockreview_qs:
                blockreview_qs = BlockReview.objects.filter(city__isnull=True)
            blockexample_qs = BlockExample.objects.filter(city=current_city)
            if not blockexample_qs:
                blockexample_qs = BlockExample.objects.filter(city__isnull=True)
        else:
            setup = Setup.objects.filter(city__isnull=True).first()
            blockeffective_qs = BlockEffective.objects.filter(city__isnull=True)
            blockreview_qs = BlockReview.objects.filter(city__isnull=True)
            blockexample_qs = BlockExample.objects.filter(city__isnull=True)
        blockexample_qs_1 = blockexample_qs[:15]
        blockexample_qs_2 = blockexample_qs[15:]
        context.update({
            'blockexample_list_1': blockexample_qs_1,
            'blockexample_list_2': blockexample_qs_2,
            'blockeffective_list': blockeffective_qs,
            'blockreview_list': blockreview_qs,
            'current_city': current_city,
            'setup': setup,
            'city_list': city_qs,
            # 'city_list_1': city_list_1,
            # 'city_list_2': city_list_2,
            'cache_time': 1800
        })
        return context


def home_view(request):
    context = {}
    city_qs = City.objects.all()
    current_city = get_object_or_None(City, slug=request.subdomain)
    if current_city:
        try:
            setup = Setup.objects.get(city=current_city)
        except:
            setup = Setup.objects.filter(city__isnull=True).first()
        blockeffective_qs = BlockEffective.objects.filter(city=current_city)
        if not blockeffective_qs:
            blockeffective_qs = BlockEffective.objects.filter(city__isnull=True)
        blockreview_qs = BlockReview.objects.filter(city=current_city)
        if not blockreview_qs:
            blockreview_qs = BlockReview.objects.filter(city__isnull=True)
        blockexample_qs = BlockExample.objects.filter(city=current_city)
        if not blockexample_qs:
            blockexample_qs = BlockExample.objects.filter(city__isnull=True)
    else:
        setup = Setup.objects.filter(city__isnull=True).first()
        blockeffective_qs = BlockEffective.objects.filter(city__isnull=True)
        blockreview_qs = BlockReview.objects.filter(city__isnull=True)
        blockexample_qs = BlockExample.objects.filter(city__isnull=True)
    blockexample_qs_1 = blockexample_qs[:15]
    blockexample_qs_2 = blockexample_qs[15:]
    context.update({
        'blockexample_list_1': blockexample_qs_1,
        'blockexample_list_2': blockexample_qs_2,
        'blockeffective_list': blockeffective_qs,
        'blockreview_list': blockreview_qs,
        'current_city': current_city,
        'setup': setup,
        'city_list': city_qs,
        # 'city_list_1': city_list_1,
        # 'city_list_2': city_list_2,
        'cache_time': 1800
    })
    return render(request, 'landing/index.html', context)


def setup_list(request):
    user = request.user
    qs = Setup.objects.all()
    if user.type == 2:
        qs = qs.filter(city__moderator=user)
    context = {
        'object_list': qs
    }
    return render(request, 'landing/setup_list.html', context)


def setup_add(request):
    """
    Добавление настроек сайта
    """
    context = {}
    user = request.user
    if request.method == 'POST':
        form = SetupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('setup-list'))
        else:
            context.update({
                'error': u'Проверьте правильность ввода полей'
            })
    else:
        form = SetupForm()
    if user.type == 2:
        form.fields['city'].queryset = City.objects.filter(moderator=user)
    context = {
        'form': form
    }
    return render(request, 'landing/setup_form.html', context)


def setup_update(request, pk):
    """
    Редактирование настроек сайта
    """
    context = {}
    instance = Setup.objects.get(pk=int(pk))
    user = request.user
    if request.method == 'POST':
        form = SetupForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('setup-list'))
        else:
            context.update({
                'error': u'Проверьте правильность ввода полей'
            })
    else:
        form = SetupForm(instance=instance)
    if user.type == 2:
        form.fields['city'].queryset = City.objects.filter(moderator=user)
    context.update({
        'object': instance,
        'form': form
    })
    return render(request, 'landing/setup_form.html', context)


def block_list(request):
    """
    Отображение списка редактируемых блоков
    """
    context = {}
    return render(request, 'landing/block_list.html', context)


def blockeffective_list(request):
    """
    Вывод списка элементов блока "Почему реклама на подъездах так эффективна"
    """
    qs = BlockEffective.objects.all()
    if request.user.type == 2:
        qs = qs.filter(city__moderator=request.user)
    context = {
        'object_list': qs
    }
    return render(request, 'landing/blockeffective_list.html', context)


def blockeffective_add(request):
    """
    Добавление элемента в блоке "Почему реклама на подъездах так эффективна"
    """
    context = {}
    if request.method == 'POST':
        form = BlockEffectiveForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('blockeffective-list'))
        else:
            context.update({
                'error': u'Ошибка! Проверьте правильность ввода данных.'
            })
    else:
        form = BlockEffectiveForm()
    if request.user.type == 2:
        form.fields['city'].queryset = City.objects.filter(moderator=request.user)
    context.update({
        'form': form
    })
    return render(request, 'landing/blockeffective_form.html', context)


def blockeffective_update(request, pk):
    """
    Редактирование элемента в блок "Почему реклама в лифтах так эффективна"
    """
    context = {}
    instance = BlockEffective.objects.get(pk=int(pk))
    if request.method == 'POST':
        form = BlockEffectiveForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('blockeffective-list'))
        else:
            context.update({
                'error': u'Ошибка! Проверьте правильность ввода данных.'
            })
    else:
        form = BlockEffectiveForm(instance=instance)
    if request.user.type == 2:
        form.fields['city'].queryset = City.objects.filter(moderator=request.user)
    context.update({
        'object': instance,
        'form': form
    })
    return render(request, 'landing/blockeffective_form.html', context)


def blockreview_list(request):
    """
    Вывод списка элементов блока "Отзывы об эффективности нашей рекламы"
    """
    qs = BlockReview.objects.all()
    if request.user.type == 2:
        qs = qs.filter(city__moderator=request.user)
    context = {
        'object_list': qs
    }
    return render(request, 'landing/blockreview_list.html', context)


def blockreview_add(request):
    """
    Добавление элемента в блок "Отзывы об эффективности нашей рекламы"
    """
    context = {}
    if request.method == 'POST':
        form = BlockReviewForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('blockreview-list'))
        else:
            context.update({
                'error': u'Ошибка! Проверьте правильность ввода данных.'
            })
    else:
        form = BlockReviewForm()
    if request.user.type == 2:
        form.fields['city'].queryset = City.objects.filter(moderator=request.user)
    context.update({
        'form': form
    })
    return render(request, 'landing/blockreview_form.html', context)


def blockreview_update(request, pk):
    """
    Редактирование элемента в блоке "Отзывы об эффективности нашей рекламы"
    """
    context = {}
    instance = BlockReview.objects.get(pk=int(pk))
    if request.method == 'POST':
        form = BlockReviewForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('blockreview-list'))
        else:
            context.update({
                'error': u'Ошибка! Проверьте правильность ввода данных.'
            })
    else:
        form = BlockReviewForm(instance=instance)
    if request.user.type == 2:
        form.fields['city'].queryset = City.objects.filter(moderator=request.user)
    context.update({
        'object': instance,
        'form': form
    })
    return render(request, 'landing/blockreview_form.html', context)


def blockexample_list(request):
    """
    Вывод списка элементов блока "Примеры размещений"
    """
    qs = BlockExample.objects.all()
    if request.user.type == 2:
        qs = qs.filter(city__moderator=request.user)
    context = {
        'object_list': qs
    }
    return render(request, 'landing/blockexample_list.html', context)


def blockexample_add(request):
    """
    Добавление элемента в блок "Примеры размещений"
    """
    context = {}
    user = request.user
    if request.method == 'POST':
        form = BlockExampleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('blockexample-list'))
        else:
            context.update({
                'error': u'Ошибка! Проверьте правильность ввода данных.'
            })
    else:
        form = BlockExampleForm()
    if user.type == 2:
        form.fields['city'].queryset = City.objects.filter(moderator=user)
    context.update({
        'form': form
    })
    return render(request, 'landing/blockexample_form.html', context)


def blockexample_update(request, pk):
    """
    Добавление элемента в блоке "Примеры размещений"
    """
    context = {}
    user = request.user
    instance = BlockExample.objects.get(pk=int(pk))
    if request.method == 'POST':
        form = BlockExampleForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('blockexample-list'))
        else:
            context.update({
                'error': u'Ошибка! Проверьте правильность ввода данных.'
            })
    else:
        form = BlockExampleForm(instance=instance)
    if user.type == 2:
        form.fields['city'].queryset = City.objects.filter(moderator=user)
    context.update({
        'object': instance,
        'form': form
    })
    return render(request, 'landing/blockexample_form.html', context)