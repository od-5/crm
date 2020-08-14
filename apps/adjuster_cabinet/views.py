# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from apps.adjuster.models import AdjusterTask, AdjusterTaskSurface, Adjuster, AdjusterTaskSurfacePorch
from apps.surface.forms import PorchAddForm, SurfacePhotoForm

__author__ = 'alexy'


@login_required
def task_list(request):
    """
    Вывод списка актуальных задач монтажника
    """
    context = {}
    user = request.user
    if user.type == 4:
        qs = AdjusterTask.objects.select_related().filter(is_closed=False, adjuster__user=user)
        context.update({
            'object_list': qs
        })
        return render(request, 'adjuster_cabinet/task_list.html', context)
    else:
        return HttpResponseRedirect(reverse('cabinet:cabinet'))


@login_required
def task_detail(request, pk):
    task = AdjusterTask.objects.select_related().get(pk=int(pk))
    address_qs = task.adjustertasksurface_set.filter(is_closed=False)
    if not address_qs:
        return HttpResponseRedirect(reverse('work:list'))
    context = {
        'task': task,
        'address_list': address_qs
    }
    return render(request, 'adjuster_cabinet/task_detail.html', context)


@login_required
def address_detail(request, pk):
    porch_qs = AdjusterTaskSurfacePorch.objects.filter(adjustertasksurface=int(pk))
    task = porch_qs.first().adjustertasksurface.adjustertask
    if not porch_qs.filter(is_closed=False):
        return HttpResponseRedirect(reverse('work:detail', args=(task.id, )))
    context = {
        'task': task,
        'object_list': porch_qs.filter(is_closed=False)
    }
    return render(request, 'adjuster_cabinet/address_detail.html', context)


@login_required
def porch_detail(request, pk):
    aporch = AdjusterTaskSurfacePorch.objects.get(pk=int(pk))
    task = aporch.adjustertasksurface.adjustertask
    has_photo = request.GET.get('has_photo')
    is_closed = request.GET.get('is_closed')
    if is_closed:
        aporch.is_closed = True
        aporch.complete = True
        aporch.save()
        return HttpResponseRedirect(reverse('work:address-detail', args=(aporch.adjustertasksurface.id,)))
    if request.method == 'POST':
        form = PorchAddForm(request.POST, instance=aporch.porch)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('work:porch-photo-add', args=(aporch.id,)))
    else:
        form = PorchAddForm(instance=aporch.porch)
    context = {
        'task': task,
        'porch_form': form,
        'object': aporch,
        'has_photo': has_photo
    }
    return render(request, 'adjuster_cabinet/porch_detail.html', context)


@login_required
def photo_add(request, pk):
    context = {}
    aporch = AdjusterTaskSurfacePorch.objects.get(pk=int(pk))
    if request.method == 'POST':
        form = SurfacePhotoForm(request.POST, request.FILES)
        if form.is_valid():
            url = '?'.join((reverse('work:porch-detail', args=(aporch.id,)), 'has_photo=1'))
            form.save()
            return HttpResponseRedirect(url)
    else:
        form = SurfacePhotoForm(initial={
            'porch': aporch.porch,
            'is_broken': aporch.porch.is_broken
        })
    context.update({
        'object': aporch,
        'form': form
    })
    return render(request, 'adjuster_cabinet/photo_add.html', context)
