# coding=utf-8
from annoying.functions import get_object_or_None
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView, UpdateView
from apps.city.models import City
from .forms import SetupForm, BlockEffectiveForm, BlockExampleForm, BlockReviewForm
from .models import Setup, BlockEffective, BlockReview, BlockExample

__author__ = 'alexy'


class LandingView(TemplateView):
    template_name = 'landing/index.html'

    def get_context_data(self, **kwargs):
        context = {}
        city_qs = City.objects.values('id', 'name', 'slug')
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
        context.update({
            'blockexample_list': blockexample_qs,
            'blockeffective_list': blockeffective_qs,
            'blockreview_list': blockreview_qs,
            'current_city': current_city,
            'setup': setup,
            'city_list': city_qs,
            'cache_time': 1800,
            'main_setup': Setup.objects.filter(city__isnull=True).values('top_js', 'bottom_js').first()
        })
        return context


class OkView(TemplateView):
    template_name = 'landing/ok.html'

    def get_context_data(self, **kwargs):
        context = super(OkView, self).get_context_data(**kwargs)
        city_qs = City.objects.values('id', 'name', 'slug')
        current_city = get_object_or_None(City, slug=self.request.subdomain)
        if current_city:
            try:
                setup = Setup.objects.get(city=current_city)
            except:
                setup = Setup.objects.filter(city__isnull=True).first()
        else:
            setup = Setup.objects.filter(city__isnull=True).first()
        context.update({
            'setup': setup,
            'city_list': city_qs,
            'cache_time': 1800,
        })
        return context


class NoOkView(TemplateView):
    template_name = 'landing/no_ok.html'

    def get_context_data(self, **kwargs):
        context = super(NoOkView, self).get_context_data(**kwargs)
        city_qs = City.objects.values('id', 'name', 'slug')
        current_city = get_object_or_None(City, slug=self.request.subdomain)
        if current_city:
            try:
                setup = Setup.objects.get(city=current_city)
            except:
                setup = Setup.objects.filter(city__isnull=True).first()
        else:
            setup = Setup.objects.filter(city__isnull=True).first()
        context.update({
            'setup': setup,
            'city_list': city_qs,
            'cache_time': 1800,
        })
        return context


class SiteSetupList(ListView):
    model = Setup
    template_name = 'landing/setup_list.html'

    def get_queryset(self):
        if self.request.user.type == 1:
            qs = self.model.objects.all()
        elif self.request.user.type == 2:
            qs = self.model.objects.filter(city__moderator=self.request.user)
        else:
            qs = self.model.objects.none()
        return qs


class SetupCreateView(CreateView):
    model = Setup
    form_class = SetupForm
    template_name = 'landing/setup_form.html'
    success_url = reverse_lazy('setup-list')

    def get_form_kwargs(self):
        kwargs = super(SetupCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class SetupUpdateView(UpdateView):
    model = Setup
    form_class = SetupForm
    template_name = 'landing/setup_form.html'
    success_url = reverse_lazy('setup-list')

    def get_form_kwargs(self):
        kwargs = super(SetupUpdateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


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