# coding=utf-8
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from core.forms import SetupForm, BlockEffectiveForm, BlockExampleForm, BlockReviewForm
from core.models import Setup, BlockEffective, BlockExample, BlockReview

__author__ = 'alexy'


def get_robots_txt(request):
    """
    Функция отображения robots.txt
    """
    try:
        content = Setup.objects.all()[0].robots_txt
    except:
        content = u'User-agent: *'
    robots_response = HttpResponse(content, content_type='text/plain')
    return robots_response


def site_config_view(request):
    """
    Функция отображения формы редактирования настроек основного сайта
    """
    context = {}
    user = request.user
    setup_qs = Setup.objects.all()
    try:
        setup_instance = Setup.objects.get(pk=setup_qs.first().id)
        print setup_instance.id
        print 'has'
    except:
        print 'Not. Need to create.'
        setup_instance = Setup(
            email=user.email,
            phone='',
            meta_title='',
            meta_desc='',
            meta_keys='',
            video='',
            top_js='',
            bottom_js='',
            robots_txt='',

        )
        setup_instance.save()
    print setup_instance
    if request.method == 'POST':
        form = SetupForm(request.POST, instance=setup_instance)
        if form.is_valid():
            form.save()
    else:
        form = SetupForm(instance=setup_instance)
    context.update({
        'form': form
    })
    return render(request, 'core/site_config.html', context)


def block_effective_add_view(request):
    context = {}
    if request.method == 'POST':
        form = BlockEffectiveForm(request.POST, request.FILES)
        print form
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('block_effective'))
        else:
            context.update({
                'error': u'Ошибка! Проверьте правильность ввода данных.'
            })
    else:
        form = BlockEffectiveForm()
    context.update({
        'form': form
    })
    return render(request, 'core/block_effective_form.html', context)


def block_effective_update_view(request, pk):
    context = {}
    instance = BlockEffective.objects.get(pk=int(pk))
    if request.method == 'POST':
        form = BlockEffectiveForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('block_effective'))
        else:
            context.update({
                'error': u'Ошибка! Проверьте правильность ввода данных.'
            })
    else:
        form = BlockEffectiveForm(instance=instance)
    context.update({
        'object': instance,
        'form': form
    })
    return render(request, 'core/block_effective_form.html', context)


def block_effective_view(request):
    context = {
        'object_list': BlockEffective.objects.all()
    }
    return render(request, 'core/block_effective_list.html', context)


def block_example_add_view(request):
    context = {}
    if request.method == 'POST':
        form = BlockExampleForm(request.POST, request.FILES)
        print form
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('block_example'))
        else:
            context.update({
                'error': u'Ошибка! Проверьте правильность ввода данных.'
            })
    else:
        form = BlockExampleForm()
    context.update({
        'form': form
    })
    return render(request, 'core/block_example_form.html', context)


def block_example_update_view(request, pk):
    context = {}
    instance = BlockExample.objects.get(pk=int(pk))
    if request.method == 'POST':
        form = BlockExampleForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('block_example'))
        else:
            context.update({
                'error': u'Ошибка! Проверьте правильность ввода данных.'
            })
    else:
        form = BlockEffectiveForm(instance=instance)
    context.update({
        'object': instance,
        'form': form
    })
    return render(request, 'core/block_example_form.html', context)


def block_example_view(request):
    context = {
        'object_list': BlockExample.objects.all()
    }
    return render(request, 'core/block_example_list.html', context)


def block_review_add_view(request):
    context = {}
    if request.method == 'POST':
        form = BlockReviewForm(request.POST, request.FILES)
        print form
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('block_review'))
        else:
            context.update({
                'error': u'Ошибка! Проверьте правильность ввода данных.'
            })
    else:
        form = BlockReviewForm()
    context.update({
        'form': form
    })
    return render(request, 'core/block_review_form.html', context)


def block_review_update_view(request, pk):
    context = {}
    instance = BlockReview.objects.get(pk=int(pk))
    if request.method == 'POST':
        form = BlockReviewForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('block_review'))
        else:
            context.update({
                'error': u'Ошибка! Проверьте правильность ввода данных.'
            })
    else:
        form = BlockReviewForm(instance=instance)
    context.update({
        'object': instance,
        'form': form
    })
    return render(request, 'core/block_review_form.html', context)


def block_review_view(request):
    context = {
        'object_list': BlockReview.objects.all()
    }
    return render(request, 'core/block_review_list.html', context)


def block_list(request):
    context = {}
    return render(request, 'core/block_list.html', context)
