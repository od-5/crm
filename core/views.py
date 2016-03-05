# coding=utf-8
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from core.forms import SetupForm
from core.models import Setup

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
