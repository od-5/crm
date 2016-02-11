# coding=utf-8
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from apps.adjuster.models import SurfacePhoto
from .forms import SurfaceAddForm, PorchAddForm, SurfacePhotoForm
from apps.city.models import City, Area, Surface, Street, Porch, ManagementCompany

__author__ = 'alexy'


class SurfaceListView(ListView):
    model = Surface
    template_name = 'surface/surface_list.html'
    paginate_by = 50

    def get_queryset(self):
        """
        Если пользователь администратор - ему доступны всё города.
        Если пользователь модератор - ему доступны только те города, которыми он управляет.
        """
        user_id = self.request.user.id
        if self.request.user.type == 1:
            qs = Surface.objects.all()
        elif self.request.user.type == 2:
            qs = Surface.objects.filter(city__moderator=user_id)
        else:
            qs = None
        # фильтрация поверхностей по городам, районам, улицам
        if self.request.GET.get('management') and int(self.request.GET.get('management')) != 0:
            qs = qs.filter(management=int(self.request.GET.get('management')))
        if self.request.GET.get('city') and int(self.request.GET.get('city')) != 0:
            qs = qs.filter(city=int(self.request.GET.get('city')))
        if self.request.GET.get('area') and int(self.request.GET.get('area')) != 0:
            qs = qs.filter(street__area=int(self.request.GET.get('area')))
        if self.request.GET.get('street') and int(self.request.GET.get('street')) != 0:
            qs = qs.filter(street=int(self.request.GET.get('street')))
        return qs

    def get_context_data(self, **kwargs):
        context = super(SurfaceListView, self).get_context_data(**kwargs)
        user_id = self.request.user.id
        """
        Администратор может выбирать любой город системы.
        Модератор - только те города, которыми он управляет.
        """
        if self.request.user.type == 1:
            qs = City.objects.all()
            management_qs = ManagementCompany.objects.all()
        elif self.request.user.type == 2:
            qs = City.objects.filter(moderator=user_id)
            management_qs = ManagementCompany.objects.filter(city__moderator=user_id)
        else:
            qs = None
            management_qs = None
        context.update({
            'city_list': qs,
            'management_list': management_qs
        })

        if self.request.GET.get('city'):
            area_qs = Area.objects.filter(city__id=int(self.request.GET.get('city')))
            context.update({
                'area_list': area_qs,
                'city_id': int(self.request.GET.get('city'))
            })
            if self.request.GET.get('area'):
                street_qs = Street.objects.filter(area__id=int(self.request.GET.get('area')))
                context.update({
                    'street_list': street_qs,
                    'area_id': int(self.request.GET.get('area'))
                })
                if self.request.GET.get('street'):
                    context.update({
                        'street_id': int(self.request.GET.get('street'))
                    })
        if self.request.GET.get('management'):
            context.update({
                'management_id': int(self.request.GET.get('management'))
            })

        return context


class SurfaceCreateView(CreateView):
    model = Surface
    form_class = SurfaceAddForm
    template_name = 'surface/surface_add.html'

    def get_initial(self):
        """
        Добавление request.user в форму, для ограничения
        в зависимости от уровня доступа пользователя
        """
        initial = super(SurfaceCreateView, self).get_initial()
        user = self.request.user
        initial = initial.copy()
        initial['user'] = self.request.user
        return initial


class SurfaceUpdateView(UpdateView):
    model = Surface
    template_name = 'surface/surface_update.html'
    form_class = SurfaceAddForm

    def get_initial(self):
        """
        Добавление request.user в форму, для ограничения
        в зависимости от уровня доступа пользователя
        """
        initial = super(SurfaceUpdateView, self).get_initial()
        user = self.request.user
        initial = initial.copy()
        initial['user'] = self.request.user
        return initial

    def get_context_data(self, **kwargs):
        context = super(SurfaceUpdateView, self).get_context_data(**kwargs)
        context.update({
            'surface': self.object
        })
        return context


class SurfacePhotoDeleteView(DeleteView):
    model = SurfacePhoto
    template_name = 'surface/surface_photo_delete.html'
    success_url = '/surface/'

    def get_context_data(self, **kwargs):
        context = super(SurfacePhotoDeleteView, self).get_context_data(**kwargs)
        context.update({
            'surface': self.object.porch.surface
        })
        return context


def surface_porch(request, pk):
    context = {}
    surface = Surface.objects.get(pk=int(pk))
    context.update({
        'surface': surface
    })
    if request.method == 'POST':
        form = PorchAddForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('surface:porch', args=(surface.id, )))
        else:
            return HttpResponseRedirect(reverse('surface:porch', args=(surface.id, )))
    else:
        form = PorchAddForm(
            initial={
                'surface': surface
            }
        )
    context.update({
        'porch_form': form
    })
    return render(request, 'surface/surface_porch.html', context)


def surface_porch_update(request, pk):
    context = {}
    porch = Porch.objects.get(pk=int(pk))
    if request.method == 'POST':
        form = PorchAddForm(request.POST, instance=porch)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('surface:porch', args=(porch.surface.id, )))
        else:
            return HttpResponseRedirect(reverse('surface:porch', args=(porch.surface.id, )))
    else:
        form = PorchAddForm(instance=porch)
    photo_form = SurfacePhotoForm(initial={
        'porch': porch
    })
    photo_qs = porch.surfacephoto_set.all()
    paginator = Paginator(photo_qs, 20)
    page = request.GET.get('page')
    try:
        photo_list = paginator.page(page)
    except PageNotAnInteger:
        photo_list = paginator.page(1)
    except EmptyPage:
        photo_list = paginator.page(paginator.num_pages)
    context.update({
        'object': porch,
        'surface': porch.surface,
        'photo_list': photo_list,
        'porch_form': form,
        'photo_form': photo_form
    })
    return render(request, 'surface/surface_porch_update.html', context)


def surface_photo_add(request):
    if request.method == 'POST':
        form = SurfacePhotoForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            return HttpResponseRedirect(reverse('surface:porch-update', args=(instance.porch.id, )))
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def surface_photo_update(request, pk):
    context = {}
    photo = SurfacePhoto.objects.get(pk=int(pk))
    success_msg = u''
    error_msg = u''
    print 'step 1'
    if request.method == 'POST':
        form = SurfacePhotoForm(request.POST, request.FILES, instance=photo)
        print form
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('surface:porch-update', args=(photo.porch.id, )))
    else:
        print 'step else'
        form = SurfacePhotoForm(instance=photo, initial={
            'file': photo.image.file
        })
    context.update({
        'success': success_msg,
        'error': error_msg,
        'photo_form': form,
        'object': photo,
        'surface': photo.porch.surface
    })
    return render(request, 'surface/surface_photo_update.html', context)
