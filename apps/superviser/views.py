# coding=utf-8
from annoying.functions import get_object_or_None
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView
from apps.superviser.models import Superviser
from .forms import SuperviserAddForm, SuperviserUpdateForm, SuperviserCityForm
from core.models import User

__author__ = 'alexy'


class SuperviserListView(ListView):
    queryset = User.objects.filter(type=2)
    template_name='superviser/superviser_list.html'
    paginate_by = 50

    def get_queryset(self):
        qs = User.objects.filter(type=6)
        if self.request.GET.get('email'):
            qs = qs.filter(email=self.request.GET.get('email'))
        if self.request.GET.get('last_name'):
            qs = qs.filter(last_name=self.request.GET.get('last_name'))
        if self.request.GET.get('first_name'):
            qs = qs.filter(first_name=self.request.GET.get('first_name'))
        if self.request.GET.get('patronymic'):
            qs = qs.filter(patronymic=self.request.GET.get('patronymic'))
        if self.request.GET.get('phone'):
            qs = qs.filter(phone=self.request.GET.get('phone'))
        return qs

    def get_context_data(self, **kwargs):
        context = super(SuperviserListView, self).get_context_data(**kwargs)
        context.update({
            'r_email': self.request.GET.get('email', ''),
            'r_last_name': self.request.GET.get('last_name', ''),
            'r_first_name': self.request.GET.get('first_name', ''),
            'r_patronymic': self.request.GET.get('patronymic', ''),
            'r_phone': self.request.GET.get('phone', '')
        })
        return context


@login_required
def superviser_add(request):
    context = {}
    if request.method == "POST":
        form = SuperviserAddForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.type = 6
            user.save()
            try:
                subject = u'Создана учётная запись nadomofone.ru'
                message = u'Для вас создана учётная запись на сайте http://nadomofone.ru\n email: %s, \n пароль: %s' % (request.POST.get('email'), request.POST.get('password1'))
                email = request.POST.get('email')
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email, ]
                )
            except:
                pass
            return HttpResponseRedirect(reverse('superviser:update', args=(user.id, )))
        else:
            context.update({
                'error': u'Проверьте правильность ввода полей'
            })
    else:
        form = SuperviserAddForm()
    context.update({
        'form': form,
    })
    return render(request, 'superviser/superviser_add.html', context)


@login_required
def superviser_update(request, pk):
    context = {}
    user = User.objects.get(pk=int(pk))
    try:
        superviser = Superviser.objects.get(superviser=user)
    except:
        superviser = Superviser(
            superviser=user
        )
        superviser.save()
    success_msg = u''
    error_msg = u''
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 and password2:
            if password1 == password2:
                user.set_password(password1)
                success_msg = u'Пароль успешно изменён!'
            else:
                error_msg = u'Пароль и подтверждение пароля не совпадают!'
        form = SuperviserUpdateForm(request.POST, instance=user)
        city_form = SuperviserCityForm(request.POST, instance=superviser)
        if form.is_valid():
            form.save()
            success_msg += u' Изменения успешно сохранены'
        else:
            error_msg = u'Проверьте правильность ввода полей!'
        if city_form.is_valid():
            city_form.save()
            success_msg += u' Изменения успешно сохранены'
        else:
            error_msg = u'Проверьте правильность ввода полей!'

    else:
        form = SuperviserUpdateForm(instance=user)
        city_form = SuperviserCityForm(instance=superviser)
    context.update({
        'success': success_msg,
        'error': error_msg,
        'form': form,
        'city_form': city_form,
        'object': user
    })
    return render(request, 'superviser/superviser_update.html', context)
