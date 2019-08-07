# coding=utf-8
from datetime import datetime
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.forms import HiddenInput
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView
from apps.adjuster.models import AdjusterTask, AdjusterTaskSurface, Adjuster, AdjusterTaskSurfacePorch
from apps.manager.models import Manager
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
        qs = AdjusterTask.objects.select_related().filter(is_closed=False)
    elif user.type == 6:
        qs = AdjusterTask.objects.select_related().filter(
            is_closed=False, adjuster__city__in=user.superviser.city_id_list())
    elif user.type == 2:
        qs = AdjusterTask.objects.select_related().filter(is_closed=False, adjuster__city__moderator=user)
    elif user.type == 4:
        qs = AdjusterTask.objects.select_related().filter(is_closed=False, adjuster__user=user)
    elif user.type == 5:
        qs = AdjusterTask.objects.select_related().filter(
            is_closed=False, adjuster__city__moderator=user.manager.moderator)
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
    if user.type == 6:
        filter_form.fields['city'].queryset = user.superviser.city.all()
        filter_form.fields['adjuster'].queryset = Adjuster.objects.filter(city__in=user.superviser.city.all())
    elif user.type == 2:
        filter_form.fields['city'].queryset = City.objects.filter(moderator=user)
        filter_form.fields['adjuster'].queryset = Adjuster.objects.filter(city__moderator=user)
    elif user.type == 5:
        manager = Manager.objects.get(user=user)
        filter_form.fields['city'].queryset = City.objects.filter(moderator=manager.moderator)
        filter_form.fields['adjuster'].queryset = Adjuster.objects.filter(city__moderator=manager.moderator)
    context.update({
        'filter_form': filter_form
    })
    total_sum = 0
    for i in qs:
        total_sum += i.get_total_cost()

    paginator = Paginator(qs, 25)
    page = request.GET.get('page')
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)
    if request.META['QUERY_STRING']:
        request.session['adjustertask_filtered_list'] = '%s?%s' % (request.path, request.META['QUERY_STRING'])
    else:
        request.session['adjustertask_filtered_list'] = reverse('adjustertask:list')
    context.update({
        'total_sum': total_sum,
        'object_list': object_list
    })
    return render(request, 'adjustertask/adjustertask_list.html', context)


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
        elif user.type == 6:
            qs = AdjusterTask.objects.filter(is_closed=True, adjuster__city__in=user.superviser.city_id_list())
        elif user.type == 2:
            qs = AdjusterTask.objects.filter(is_closed=True, adjuster__city__moderator=user)
        elif user.type == 4:
            qs = AdjusterTask.objects.filter(is_closed=True, adjuster__user=user)
        elif user.type == 5:
            manager = Manager.objects.get(user=user)
            qs = AdjusterTask.objects.filter(is_closed=True, adjuster__city__moderator=manager.moderator)
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
        if user.type == 6:
            filter_form.fields['city'].queryset = user.superviser.city.all()
            filter_form.fields['adjuster'].queryset = Adjuster.objects.filter(city__in=user.superviser.city_id_list())
        elif user.type == 2:
            filter_form.fields['city'].queryset = City.objects.filter(moderator=user)
            filter_form.fields['adjuster'].queryset = Adjuster.objects.filter(city__moderator=user)
        elif user.type == 2:
            manager = Manager.objects.get(user=user)
            filter_form.fields['city'].queryset = City.objects.filter(moderator=manager.moderator)
            filter_form.fields['adjuster'].queryset = Adjuster.objects.filter(city__moderator=manager.moderator)
        if self.request.META['QUERY_STRING']:
            self.request.session['adjustertaskarchive_filtered_list'] = '%s?%s' % (self.request.path, self.request.META['QUERY_STRING'])
        else:
            self.request.session['adjustertaskarchive_filtered_list'] = reverse('adjustertask:archive')
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
                            if not surface.coord_x or not surface.coord_y:
                                surface.save()
                    except:
                        pass
                return HttpResponseRedirect(task.get_absolute_url())
    else:
        form = AdjusterTaskClientForm()
        if user.type == 1:
            client_qs = Client.objects.all()
        elif user.type == 6:
            client_qs = Client.objects.filter(city__in=user.superviser.city_id_list())
        elif user.type == 2:
            client_qs = Client.objects.filter(city__moderator=user)
        elif user.type == 5:
            manager = Manager.objects.get(user=user)
            client_qs = Client.objects.filter(city__moderator=manager.moderator)
        else:
            client_qs = None
        form.fields['client'].queryset = client_qs
    try:
        request.session['adjustertask_filtered_list']
    except:
        request.session['adjustertask_filtered_list'] = reverse('adjustertask:list')
    context.update({
        'form': form,
        'back_to_list': request.session['adjustertask_filtered_list']
    })
    return render(request, 'adjustertask/adjustertask_client_add.html', context)


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
                            if not surface.coord_x or not surface.coord_y:
                                surface.save()
                    except:
                        pass
                return HttpResponseRedirect(task.get_absolute_url())
            elif request.POST.getlist('chk_group2[]'):
                # сохраняем задачу
                task = form.save()
                porches = request.POST.getlist('chk_group2[]')
                for item in porches:
                    try:
                        porch = Porch.objects.get(pk=int(item))
                        try:
                            adjustertasksurface = AdjusterTaskSurface.objects.get(adjustertask=task,
                                                                                  surface=porch.surface)
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
                    except:
                        pass
                return HttpResponseRedirect(task.get_absolute_url())
    else:
        form = AdjusterTaskAreaAddForm()
        if user.type == 1:
            city_qs = City.objects.all()
        elif user.type == 6:
            city_qs = user.superviser.city.all()
        elif user.type == 2:
            city_qs = City.objects.filter(moderator=user)
        elif user.type == 5:
            manager = Manager.objects.get(user=user)
            city_qs = City.objects.filter(moderator=manager.moderator)
        else:
            city_qs = None
        form.fields['city'].queryset = city_qs
    try:
        request.session['adjustertask_filtered_list']
    except:
        request.session['adjustertask_filtered_list'] = reverse('adjustertask:list')
    context.update({
        'form': form,
        'back_to_list': request.session['adjustertask_filtered_list']
    })
    return render(request, 'adjustertask/adjustertask_area_add.html', context)


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
                    surface = porch.surface
                    if not surface.coord_x or not surface.coord_y:
                        surface.save()
                return HttpResponseRedirect(task.get_absolute_url())
            else:
                error = u'Не выбрано ни одно подъезда для ремонта'
        else:
            error = u'Проверьте правильность ввода полей. Все поля, кроме комментария, обязательны к заполнению'
    else:
        form = AdjusterTaskRepairAddForm()
    if user.type == 1:
        city_qs = City.objects.all()
    elif user.type == 6:
        city_qs = user.superviser.city.all()
    elif user.type == 2:
        city_qs = City.objects.filter(moderator=user)
    elif user.type == 5:
        city_qs = City.objects.filter(moderator=user.manager.moderator)
    else:
        city_qs = None
    form.fields['city'].queryset = city_qs
    try:
        request.session['adjustertask_filtered_list']
    except:
        request.session['adjustertask_filtered_list'] = reverse('adjustertask:list')
    context.update({
        'form': form,
        'error': error,
        'back_to_list': request.session['adjustertask_filtered_list']
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
        if int(request.POST.get('adjuster')) != adjustertask.adjuster.id:
            adjustertask.sent = False
            adjustertask.save()
        adjuster_task_form = AdjusterTaskUpdateForm(request.POST, request=request, instance=adjustertask)
        if adjuster_task_form.is_valid():
            adjuster_task_form.save()
            return HttpResponseRedirect(adjustertask.get_absolute_url())
    else:
        adjuster_task_form = AdjusterTaskUpdateForm(request=request, instance=adjustertask)
    if adjustertask.sent:
        adjuster_task_form.fields['type'].widget = HiddenInput()
        adjuster_task_form.fields['date'].widget = HiddenInput()
        adjuster_task_form.fields['comment'].widget = HiddenInput()
    try:
        request.session['adjustertask_filtered_list']
    except:
        request.session['adjustertask_filtered_list'] = reverse('adjustertask:list')
    context.update({
        'adjuster_task_form': adjuster_task_form,
        'back_to_list': request.session['adjustertask_filtered_list']
    })
    return render(request, 'adjustertask/adjustertask_update.html', context)
