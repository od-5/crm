# coding=utf-8
from datetime import datetime
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView
from apps.adjuster.forms import AdjusterAddForm, AdjusterUpdateForm, AdjusterPaymentForm
from apps.city.models import City
from apps.manager.models import Manager
from core.forms import UserAddForm, UserUpdateForm
from .models import Adjuster

__author__ = 'alexy'


class AdjusterListView(ListView):
    model = Adjuster
    paginate_by = 25

    def get_queryset(self):
        if self.request.user.type == 1:
            qs = Adjuster.objects.all()
        elif self.request.user.type == 2:
            qs = Adjuster.objects.filter(city__moderator=self.request.user)
        elif self.request.user.type == 5:
            manager = Manager.objects.get(user=self.request.user)
            qs = Adjuster.objects.filter(city__moderator=manager.moderator)
        else:
            qs = None
        if self.request.GET.get('email'):
            qs = qs.filter(user__email=self.request.GET.get('email'))
        if self.request.GET.get('last_name'):
            qs = qs.filter(user__last_name=self.request.GET.get('last_name'))
        if self.request.GET.get('city') and int(self.request.GET.get('city')) != 0:
            qs = qs.filter(city__id=int(self.request.GET.get('city')))
        return qs

    def get_context_data(self, **kwargs):
        context = super(AdjusterListView, self).get_context_data()
        if self.request.user.type == 1:
            city_qs = City.objects.all()
        elif self.request.user.type == 2:
            city_qs = City.objects.filter(moderator=self.request.user)
        elif self.request.user.type == 5:
            manager = Manager.objects.get(user=self.request.user)
            city_qs = City.objects.filter(moderator=manager.moderator)
        else:
            city_qs = None
        context.update({
            'city_list': city_qs
        })
        if self.request.GET.get('city'):
            context.update({
                'city_id': int(self.request.GET.get('city'))
            })
        if self.request.GET.get('email'):
            context.update({
                'r_email': self.request.GET.get('email')
            })
        if self.request.GET.get('last_name'):
            context.update({
                'r_last_name': self.request.GET.get('last_name')
            })
        return context


def adjuster_add(request):
    context = {}
    if request.method == "POST":
        user_form = UserAddForm(request.POST)
        adjuster_form = AdjusterAddForm(request.POST, request=request)
        if user_form.is_valid() and adjuster_form.is_valid():
            # TODO: сделать отправку сообщения о регистрации на email
            user = user_form.save(commit=False)
            user.type = 4
            user.save()
            adjuster = adjuster_form.save(commit=False)
            adjuster.user = user
            adjuster.save()
            return HttpResponseRedirect(reverse('adjuster:change', args=(adjuster.id, )))
        else:
            context.update({
                'error': u'Проверьте правильность ввода полей'
            })
    else:
        user_form = UserAddForm()
        adjuster_form = AdjusterAddForm(request=request)
    context.update({
        'user_form': user_form,
        'adjuster_form': adjuster_form
    })
    return render(request, 'adjuster/adjuster_add.html', context)


def adjuster_update(request, pk):
    context = {}
    adjuster = Adjuster.objects.get(pk=int(pk))
    user = adjuster.user
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
        user_form = UserUpdateForm(request.POST, instance=user)
        adjuster_form = AdjusterUpdateForm(request.POST, request=request, instance=adjuster)
        if user_form.is_valid() and adjuster_form.is_valid():
            user_form.save()
            adjuster_form.save()
            success_msg += u' Изменения успешно сохранены'
        else:
            error_msg = u'Проверьте правильность ввода полей!'
    else:
        user_form = UserUpdateForm(instance=user)
        adjuster_form = AdjusterUpdateForm(request=request, instance=adjuster)
    context.update({
        'success': success_msg,
        'error': error_msg,
        'user_form': user_form,
        'adjuster_form': adjuster_form,
        'adjuster': adjuster
    })
    return render(request, 'adjuster/adjuster_update.html', context)


def adjuster_task(request, pk):
    context = {}
    r_date_s = request.GET.get('date_s')
    r_date_e = request.GET.get('date_e')
    context.update({
        'r_date_s': r_date_s,
        'r_date_e': r_date_e
    })
    adjuster = Adjuster.objects.get(pk=int(pk))
    qs = adjuster.adjustertask_set.all()
    if r_date_s:
        qs = qs.filter(date__gte=datetime.strptime(r_date_s, '%d.%m.%Y'))
    if r_date_e:
        qs = qs.filter(date__lte=datetime.strptime(r_date_e, '%d.%m.%Y'))
    total_sum = 0
    for i in qs:
        total_sum += i.get_actual_cost()
    paginator = Paginator(qs, 25)
    page = request.GET.get('page')
    try:
        task_list = paginator.page(page)
    except PageNotAnInteger:
        task_list = paginator.page(1)
    except EmptyPage:
        task_list = paginator.page(paginator.num_pages)
    context.update({
        'adjuster': adjuster,
        'task_list': task_list,
        'total_sum': total_sum
    })
    return render(request, 'adjuster/adjuster_task.html', context)


def adjuster_payment(request, pk):
    adjuster = Adjuster.objects.get(pk=int(pk))
    context = {
        'adjuster': adjuster
    }
    if request.method == 'POST':
        form = AdjusterPaymentForm(request.POST, instance=adjuster)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adjuster:change', args=(adjuster.id, )))
    else:
        form = AdjusterPaymentForm(instance=adjuster)
    context.update({
        'form': form
    })
    return render(request, 'adjuster/adjuster_payment.html', context)
