# coding=utf-8
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView
from apps.adjuster.models import AdjusterTask, AdjusterTaskSurface
from apps.adjustertask.forms import AdjusterTaskClientAddForm, AdjusterTaskAddForm, AdjusterTaskUpdateForm
from apps.city.models import Surface

__author__ = 'alexy'


class AdjusterTaskListView(ListView):
    model = AdjusterTask
    template_name = 'adjustertask/adjustertask_list.html'

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


def adjuster_task_add(request):
    context = {}
    if request.method == 'POST':
        adjustertask_client_form = AdjusterTaskClientAddForm(request.POST, request=request)
        adjustertask_form = AdjusterTaskAddForm(request.POST, request=request)
        if adjustertask_client_form.is_valid():
            if request.POST.getlist('chk_group[]'):
                task = adjustertask_client_form.save()
                surfaces = request.POST.getlist('chk_group[]')
                for item in surfaces:
                    surface = Surface.objects.get(pk=int(item))
                    task_surface = AdjusterTaskSurface(
                        adjustertask=task,
                        surface=surface
                    )
                    task_surface.save()
                return HttpResponseRedirect(task.get_absolute_url())
        else:
            context.update({
                'error': 'Achtung! Form is invalid!'
            })
    else:
        adjustertask_client_form = AdjusterTaskClientAddForm(request=request)
        adjustertask_form = AdjusterTaskAddForm(request=request)
    context.update({
        'adjustertask_client_form': adjustertask_client_form,
        'adjustertask_form': adjustertask_form
    })
    return render(request, 'adjustertask/adjustertask_add.html', context)


def adjuster_simple_task_add(request):
    context = {}
    if request.method == 'POST':
        adjustertask_form = AdjusterTaskAddForm(request.POST, request=request)
        if adjustertask_form.is_valid():
            if request.POST.getlist('chk_group_1[]'):
                task = adjustertask_form.save()
                surfaces = request.POST.getlist('chk_group_1[]')
                for item in surfaces:
                    surface = Surface.objects.get(pk=int(item))
                    task_surface = AdjusterTaskSurface(
                        adjustertask=task,
                        surface=surface
                    )
                    task_surface.save()
                return HttpResponseRedirect(task.get_absolute_url())
        else:
            return HttpResponseRedirect(reverse('adjustertask:add'))
    else:
        return HttpResponseRedirect(reverse('adjustertask:add'))


def adjuster_task_update(request, pk):
    context = {}
    adjustertask = AdjusterTask.objects.get(pk=int(pk))
    context.update({
        'object': adjustertask
    })
    if request.method == "POST":
        adjuster_task_form = AdjusterTaskUpdateForm(request.POST, request=request, instance=adjustertask)
        if adjuster_task_form.is_valid():
            adjuster_task_form.save()
            return HttpResponseRedirect(adjustertask.get_absolute_url())
    else:
        adjuster_task_form = AdjusterTaskUpdateForm(request=request, instance=adjustertask)
    context.update({
        'adjuster_task_form': adjuster_task_form
    })
    return render(request, 'adjustertask/adjustertask_update.html', context)
