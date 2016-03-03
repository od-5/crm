# coding=utf-8
from datetime import datetime
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView
from apps.adjuster.models import AdjusterTask, AdjusterTaskSurface, Adjuster, AdjusterTaskSurfacePorch
from .forms import AdjusterTaskClientAddForm, AdjusterTaskAddForm, AdjusterTaskUpdateForm, \
    AdjusterTaskFilterForm, AdjusterTaskRepairAddForm, AdjusterTaskClientForm, AdjusterTaskAreaAddForm
from .task_calendar import get_months
from apps.city.models import Surface, City, Porch
from apps.client.models import Client, ClientOrder

__author__ = 'alexy'


def adjustertask_list(request):
    context = {}
    context.update(
        get_months(),
    )
    initial_args = {}
    user = request.user
    if user.type == 1:
        qs = AdjusterTask.objects.filter(is_closed=False)
    elif user.type == 2:
        qs = AdjusterTask.objects.filter(is_closed=False, adjuster__city__moderator=user)
    elif user.type == 4:
        qs = AdjusterTask.objects.filter(is_closed=False, adjuster__user=user)
    else:
        qs = None
    if request.GET.get('city'):
        qs = qs.filter(adjuster__city=int(request.GET.get('city')))
        initial_args.update({
            'city': request.GET.get('city')
        })
    if request.GET.get('adjuster'):
        qs = qs.filter(adjuster=int(request.GET.get('adjuster')))
        initial_args.update({
            'adjuster': int(request.GET.get('adjuster'))
        })
    if request.GET.get('type'):
        qs = qs.filter(type=int(request.GET.get('type')))
        initial_args.update({
            'type': int(request.GET.get('type'))
        })
    if request.GET.get('date_s'):
        qs = qs.filter(date__gte=datetime.strptime(request.GET.get('date_s'), '%d.%m.%Y'))
        initial_args.update({
            'date_s': request.GET.get('date_s')
        })
    if request.GET.get('date_e'):
        qs = qs.filter(date__lte=datetime.strptime(request.GET.get('date_e'), '%d.%m.%Y'))
        initial_args.update({
            'date_e': request.GET.get('date_e')
        })
    if request.GET.get('date__day') and request.GET.get('date__month') and request.GET.get('date__year'):
        day = request.GET.get('date__day')
        month = request.GET.get('date__month')
        year = request.GET.get('date__year')
        qs = qs.filter(date__day=day, date__month=month, date__year=year)
    filter_form = AdjusterTaskFilterForm(initial=initial_args)
    if user.type == 2:
        filter_form.fields['city'].queryset = City.objects.filter(moderator=user)
        filter_form.fields['adjuster'].queryset = Adjuster.objects.filter(city__moderator=user)
    context.update({
        'filter_form': filter_form
    })
    paginator = Paginator(qs, 25)
    page = request.GET.get('page')
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)
    context.update({
        'object_list': object_list
    })
    return render(request, 'adjustertask/adjustertask_list.html', context)


class AdjusterTaskListView(ListView):
    """
    Список задач
    """
    model = AdjusterTask
    template_name = 'adjustertask/adjustertask_list.html'
    paginate_by = 2

    def get_queryset(self):
        user_id = self.request.user.id
        if self.request.user.type == 1:
            qs = AdjusterTask.objects.filter(is_closed=False)
        elif self.request.user.type == 2:
            qs = AdjusterTask.objects.filter(is_closed=False, adjuster__city__moderator=user_id)
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
        initial_args = {}
        if self.request.GET.get('city'):
            initial_args.update({
                'city': int(self.request.GET.get('city'))
            })
        if self.request.GET.get('adjuster'):
            initial_args.update({
                'adjuster': int(self.request.GET.get('adjuster'))
            })
        if self.request.GET.get('type'):
            initial_args.update({
                'type': int(self.request.GET.get('type'))
            })
        if self.request.GET.get('date_s'):
            initial_args.update({
                'date_s': self.request.GET.get('date_s')
            })
        if self.request.GET.get('date_e'):
            initial_args.update({
                'date_e': self.request.GET.get('date_e')
            })
        filter_form = AdjusterTaskFilterForm(initial=initial_args)
        if self.request.user.type == 2:
            filter_form.fields['city'].queryset = City.objects.filter(moderator=self.request.user)
            filter_form.fields['adjuster'].queryset = Adjuster.objects.filter(city__moderator=self.request.user)
        context.update({
            'filter_form': filter_form
        })
        return context


class TaskArchiveListView(ListView):
    """
    Архив задач
    """
    model = AdjusterTask
    template_name = 'adjustertask/adjustertask_archive.html'
    paginate_by = 25

    def get_queryset(self):
        user = self.request.user
        if user.type == 1:
            qs = AdjusterTask.objects.filter(is_closed=True)
        elif user.type == 2:
            qs = AdjusterTask.objects.filter(is_closed=True, adjuster__city__moderator=user)
        elif user.type == 4:
            qs = AdjusterTask.objects.filter(is_closed=True, adjuster__user=user)
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
        queryset = qs
        return queryset

    def get_context_data(self, **kwargs):
        context = super(TaskArchiveListView, self).get_context_data()
        initial_args = {}
        if self.request.GET.get('city'):
            initial_args.update({
                'city': int(self.request.GET.get('city'))
            })
        if self.request.GET.get('adjuster'):
            initial_args.update({
                'adjuster': int(self.request.GET.get('adjuster'))
            })
        if self.request.GET.get('type'):
            initial_args.update({
                'type': int(self.request.GET.get('type'))
            })
        if self.request.GET.get('date_s'):
            initial_args.update({
                'date_s': self.request.GET.get('date_s')
            })
        if self.request.GET.get('date_e'):
            initial_args.update({
                'date_e': self.request.GET.get('date_e')
            })
        filter_form = AdjusterTaskFilterForm(initial=initial_args)
        user = self.request.user
        if user.type == 2:
            filter_form.fields['city'].queryset = City.objects.filter(moderator=user)
            filter_form.fields['adjuster'].queryset = Adjuster.objects.filter(city__moderator=user)
        context.update({
            'filter_form': filter_form
        })
        return context


def adjustertask_client(request):
    """
    функция добавления задачи по клиенту
    версия 2
    """
    context = {}
    user = request.user
    if request.method == 'POST':
        form = AdjusterTaskClientForm(request.POST)
        if form.is_valid():
            if request.POST.getlist('chk_group[]'):
                # сохраняем задачу
                task = form.save()
                surfaces = request.POST.getlist('chk_group[]')
                for item in surfaces:
                    try:
                        surface = Surface.objects.get(pk=int(item))
                        # Если полностью сломана - не создавать поверхность задачи
                        # сохраняем поверхности для задачи
                        if not surface.full_broken:
                            adjustertasksurface = AdjusterTaskSurface(
                                adjustertask=task,
                                surface=surface
                            )
                            adjustertasksurface.save()
                            for porch in surface.porch_set.all():
                                if not porch.is_broken:
                                    atsporch = AdjusterTaskSurfacePorch(
                                        adjustertasksurface=adjustertasksurface,
                                        porch=porch
                                    )
                                    atsporch.save()
                    except:
                        pass
                return HttpResponseRedirect(task.get_absolute_url())
    else:
        form = AdjusterTaskClientForm()
        if user.type == 1:
            client_qs = Client.objects.all()
        elif user.type == 2:
            client_qs = Client.objects.filter(city__moderator=user)
        else:
            client_qs = None
        form.fields['client'].queryset = client_qs

    context.update({
        'form': form
    })
    return render(request, 'adjustertask/adjustertask_client_add.html', context)


def adjuster_c_task(request):
    """
    функция добавления задачи по клиенту
    версия 1
    """
    context = {}
    if request.method == 'POST':
        adjustertask_client_form = AdjusterTaskClientAddForm(request.POST, request=request)
        # adjustertask_form = AdjusterTaskAddForm(request.POST, request=request)
        if adjustertask_client_form.is_valid():
            if request.POST.getlist('chk_group[]'):
                task = adjustertask_client_form.save()
                surfaces = request.POST.getlist('chk_group[]')
                for item in surfaces:
                    try:
                        """
                        Если поверхность есть у клиента в заказе, но из системы уже удалена - нужно проверять, что бы не было ошибок
                        """
                        surface = Surface.objects.get(pk=int(item))
                        task_surface = AdjusterTaskSurface(
                            adjustertask=task,
                            surface=surface
                        )
                        task_surface.save()
                    except:
                        pass
                return HttpResponseRedirect(task.get_absolute_url())
        else:
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
    return render(request, 'adjustertask/adjustertask_c_add.html', context)


def adjustertask_area(request):
    """
    функция добавления задачи по районам
    версия 2
    """
    context = {}
    user = request.user
    if request.method == 'POST':
        form = AdjusterTaskAreaAddForm(request.POST)
        if form.is_valid():
            if request.POST.getlist('chk_group[]'):
                # сохраняем задачу
                task = form.save()
                surfaces = request.POST.getlist('chk_group[]')
                for item in surfaces:
                    try:
                        surface = Surface.objects.get(pk=int(item))
                        # Если полностью сломана - не создавать поверхность задачи
                        # сохраняем поверхности для задачи
                        if not surface.full_broken:
                            adjustertasksurface = AdjusterTaskSurface(
                                adjustertask=task,
                                surface=surface
                            )
                            adjustertasksurface.save()
                            for porch in surface.porch_set.all():
                                if not porch.is_broken:
                                    atsporch = AdjusterTaskSurfacePorch(
                                        adjustertasksurface=adjustertasksurface,
                                        porch=porch
                                    )
                                    atsporch.save()
                    except:
                        pass
                return HttpResponseRedirect(task.get_absolute_url())
    else:
        form = AdjusterTaskAreaAddForm()
        if user.type == 1:
            city_qs = City.objects.all()
        elif user.type == 2:
            city_qs = City.objects.filter(moderator=user)
        else:
            city_qs = None
        form.fields['city'].queryset = city_qs
    context.update({
        'form': form
    })
    return render(request, 'adjustertask/adjustertask_area_add.html', context)


def adjuster_a_task(request):
    """
    функция добавления задачи по адресам
    версия 1
    """
    context = {}
    if request.method == 'POST':
        adjustertask_form = AdjusterTaskAddForm(request.POST, request=request)
        if adjustertask_form.is_valid():
            if request.POST.getlist('chk_group[]'):
                task = adjustertask_form.save()
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
        adjustertask_form = AdjusterTaskAddForm(request=request)
    context.update({
        'adjustertask_form': adjustertask_form
    })
    return render(request, 'adjustertask/adjustertask_a_add.html', context)


def adjustertask_repair(request):
    """
    функция добавления задачи на ремонт
    версия 2
    """
    context = {}
    error = None
    user = request.user
    if request.method == 'POST':
        form = AdjusterTaskRepairAddForm(request.POST)
        if form.is_valid():
            if request.POST.getlist('chk_group[]'):
                task = form.save()
                porch_list = request.POST.getlist('chk_group[]')
                for item in porch_list:
                    porch = Porch.objects.get(pk=int(item))
                    try:
                        adjustertasksurface = AdjusterTaskSurface.objects.get(adjustertask=task, surface=porch.surface)
                    except:
                        adjustertasksurface = AdjusterTaskSurface(
                            adjustertask=task,
                            surface=porch.surface
                        )
                        adjustertasksurface.save()
                    atsporch = AdjusterTaskSurfacePorch(
                        adjustertasksurface=adjustertasksurface,
                        porch=porch
                    )
                    atsporch.save()
                return HttpResponseRedirect(task.get_absolute_url())
            else:
                error = u'Не выбрано ни одно подъезда для ремонта'
        else:
            error = u'Проверьте правильность ввода полей. Все поля, кроме комментария, обязательны к заполнению'
    else:
        form = AdjusterTaskRepairAddForm()
    if user.type == 1:
        city_qs = City.objects.all()
    elif user.type == 2:
        city_qs = City.objects.filter(moderator=user)
    else:
        city_qs = None
    form.fields['city'].queryset = city_qs
    context.update({
        'form': form,
        'error': error
    })
    return render(request, 'adjustertask/adjustertask_repair_add.html', context)


def adjuster_task_update(request, pk):
    """
    Обновление задачи
    """
    context = {}
    adjustertask = AdjusterTask.objects.get(pk=int(pk))
    task_surface_qs = adjustertask.adjustertasksurface_set.all()
    paginator = Paginator(task_surface_qs, 25)
    page = request.GET.get('page')
    try:
        task_surface_list = paginator.page(page)
    except PageNotAnInteger:
        task_surface_list = paginator.page(1)
    except EmptyPage:
        task_surface_list = paginator.page(paginator.num_pages)
    context.update({
        'object': adjustertask,
        'task_surface_list': task_surface_list
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
