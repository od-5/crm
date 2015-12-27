# coding=utf-8
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView
from apps.adjuster.forms import AdjusterUserAddForm, AdjusterAddForm, AdjusterUserUpdateForm, AdjusterUpdateForm, \
    AdjusterTaskAddForm
from apps.city.models import Surface
from .models import Adjuster, AdjusterTask, AdjusterTaskSurface

__author__ = 'alexy'


class AdjusterListView(ListView):
    model = Adjuster

    def get_queryset(self):
        user_id = self.request.user.id
        if self.request.user.type == 1:
            qs = Adjuster.objects.all()
        elif self.request.user.type == 2:
            qs = Adjuster.objects.filter(city__moderator=user_id)
        else:
            qs = None
        queryset = qs
        return queryset


class AdjusterTaskListView(ListView):
    model = AdjusterTask

    def get_queryset(self):
        user_id = self.request.user.id
        if self.request.user.type == 1:
            qs = AdjusterTask.objects.all()
        elif self.request.user.type == 2:
            qs = AdjusterTask.objects.filter(adjuster__city__moderator=user_id)
        else:
            qs = None
        queryset = qs
        return queryset


def adjuster_add(request):
    context = {}
    if request.method == "POST":
        user_form = AdjusterUserAddForm(request.POST)
        adjuster_form = AdjusterAddForm(request.POST, request=request)
        if user_form.is_valid() and adjuster_form.is_valid():
            user = user_form.save()
            adjuster = adjuster_form.save(commit=False)
            adjuster.user = user
            adjuster.save()
            return HttpResponseRedirect(reverse('adjuster:change', args=(adjuster.id, )))
        else:
            context.update({
                'error': u'Проверьте правильность ввода полей'
            })
    else:
        user_form = AdjusterUserAddForm()
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
        user_form = AdjusterUserUpdateForm(request.POST, instance=user)
        adjuster_form = AdjusterUpdateForm(request.POST, request=request, instance=adjuster)
        if user_form.is_valid() and adjuster_form.is_valid():
            user_form.save()
            adjuster_form.save()
            success_msg += u' Изменения успешно сохранены'
        else:
            error_msg = u'Проверьте правильность ввода полей!'
    else:
        user_form = AdjusterUserUpdateForm(instance=user)
        adjuster_form = AdjusterUpdateForm(request=request, instance=adjuster)
    context.update({
        'success': success_msg,
        'error': error_msg,
        'user_form': user_form,
        'adjuster_form': adjuster_form,
        'object': adjuster
    })
    return render(request, 'adjuster/adjuster_update.html', context)


def adjuster_task_add(request):
    context = {}
    if request.method == 'POST':
        adjuster_task_form = AdjusterTaskAddForm(request.POST, request=request)
        if adjuster_task_form.is_valid():
            if request.POST.getlist('chk_group[]'):
                task = adjuster_task_form.save()
                print task.id
                surfaces = request.POST.getlist('chk_group[]')
                for item in surfaces:
                    surface = Surface.objects.get(pk=int(item))
                    task_surface = AdjusterTaskSurface(
                        adjustertask=task,
                        surface=surface
                    )
                    task_surface.save()
                    print task_surface
        else:
            context.update({
                'error': 'Achtung! Form is invalid!'
            })
    else:
        adjuster_task_form = AdjusterTaskAddForm(request=request)
    context.update({
        'adjuster_task_form': adjuster_task_form
    })
    return render(request, 'adjuster/adjustertask_add.html', context)


def adjuster_task_update(request, pk):
    context = {}
    adjustertask = AdjusterTask.objects.get(pk=int(pk))
    adjuster_task_form = AdjusterTaskAddForm(request.POST, request=request, instance=adjustertask)
    context.update({
        'adjuster_task_form': adjuster_task_form
    })
    return render(request, 'adjuster/adjustertask_update.html', context)
