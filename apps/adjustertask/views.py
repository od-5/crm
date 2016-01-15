# coding=utf-8
from datetime import datetime
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView
from apps.adjuster.models import AdjusterTask, AdjusterTaskSurface, Adjuster
from apps.adjustertask.forms import AdjusterTaskClientAddForm, AdjusterTaskAddForm, AdjusterTaskUpdateForm, \
    AdjusterTaskFilterForm
from apps.adjustertask.task_calendar import get_months
from apps.city.models import Surface, City

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
        if self.request.GET.get('city'):
            qs = qs.filter(adjuster__city=int(self.request.GET.get('city')))
        if self.request.GET.get('adjuster'):
            qs = qs.filter(adjuster=int(self.request.GET.get('adjuster')))
        if self.request.GET.get('type'):
            qs = qs.filter(type=int(self.request.GET.get('type')))
        if self.request.GET.get('date_s'):
            qs = qs.filter(date__gte=datetime.strptime(self.request.GET.get('date_s'), '%d.%m.%Y'))
        if self.request.GET.get('date_e'):
            qs = qs.filter(date__lte=datetime.strptime(self.request.GET.get('date_e'), '%d.%m.%Y'))

        # end_date = self.request.GET.get('end_date')
        # re_date = datetime.strptime(end_date, '%d.%m.%Y')
        if self.request.GET.get('date__day') and self.request.GET.get('date__month') and self.request.GET.get('date__year'):
            day = self.request.GET.get('date__day')
            month = self.request.GET.get('date__month')
            year = self.request.GET.get('date__year')
            qs = qs.filter(date__day=day, date__month=month, date__year=year)
        queryset = qs
        return queryset

    def get_context_data(self, **kwargs):
        context = super(AdjusterTaskListView, self).get_context_data()
        context.update(
            get_months(),
        )
        filter_form = AdjusterTaskFilterForm()
        if self.request.user.type == 2:
            filter_form.fields['city'] = City.objects.filter(moderator=self.request.user)
            filter_form.fields['adjuster'] = Adjuster.objects.filter(city__moderator=self.request.user)
        context.update({
            'filter_form': filter_form
        })
        return context


def adjuster_task(request):
    context = {}
    if request.method == 'POST':
        adjustertask_client_form = AdjusterTaskClientAddForm(request.POST, request=request)
        # adjustertask_form = AdjusterTaskAddForm(request.POST, request=request)
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
            print adjustertask_client_form
            context.update({
                'error': 'Achtung! Form is invalid!'
            })
    else:
        adjustertask_client_form = AdjusterTaskClientAddForm(request=request)
        # adjustertask_form = AdjusterTaskAddForm(request=request)
    # adjustertask_client_form = AdjusterTaskClientAddForm(request=request)
    context.update({
        'adjustertask_client_form': adjustertask_client_form
    })
    return render(request, 'adjustertask/adjustertask_add.html', context)


# def adjuster_task_add(request):
#     context = {}
#     if request.method == 'POST':
#         adjustertask_client_form = AdjusterTaskClientAddForm(request.POST, request=request)
#         adjustertask_form = AdjusterTaskAddForm(request.POST, request=request)
#         if adjustertask_client_form.is_valid():
#             if request.POST.getlist('chk_group[]'):
#                 task = adjustertask_client_form.save()
#                 surfaces = request.POST.getlist('chk_group[]')
#                 for item in surfaces:
#                     surface = Surface.objects.get(pk=int(item))
#                     task_surface = AdjusterTaskSurface(
#                         adjustertask=task,
#                         surface=surface
#                     )
#                     task_surface.save()
#                 return HttpResponseRedirect(task.get_absolute_url())
#         else:
#             context.update({
#                 'error': 'Achtung! Form is invalid!'
#             })
#     else:
#         adjustertask_client_form = AdjusterTaskClientAddForm(request=request)
#         adjustertask_form = AdjusterTaskAddForm(request=request)
#     context.update({
#         'adjustertask_client_form': adjustertask_client_form,
#         'adjustertask_form': adjustertask_form
#     })
#     return render(request, 'adjustertask/adjustertask_add.html', context)


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
