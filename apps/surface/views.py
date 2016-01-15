# coding=utf-8
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from apps.adjuster.models import SurfacePhoto
from .forms import SurfaceAddForm, SurfaceClientAddForm, PorchAddForm, SurfacePhotoForm
from apps.city.models import City, Area, Surface, Street, Porch

__author__ = 'alexy'


class SurfaceListView(ListView):
    model = Surface
    template_name = 'surface/surface_list.html'

    def get_queryset(self):
        user_id = self.request.user.id
        if self.request.user.type == 1:
            qs = Surface.objects.all()
        elif self.request.user.type == 2:
            qs = Surface.objects.filter(city__moderator=user_id)
        else:
            qs = None
        if self.request.GET.get('city') and int(self.request.GET.get('city')) != 0:
            queryset = qs.filter(city__id=int(self.request.GET.get('city')))
            if self.request.GET.get('area') and int(self.request.GET.get('area')) != 0:
                queryset = queryset.filter(street__area__id=int(self.request.GET.get('area')))
                if self.request.GET.get('street') and int(self.request.GET.get('street')) != 0:
                    queryset = queryset.filter(street__id=int(self.request.GET.get('street')))
        else:
            queryset = qs
        return queryset

    def get_context_data(self, **kwargs):
        context = super(SurfaceListView, self).get_context_data(**kwargs)
        user_id = self.request.user.id
        if self.request.user.type == 1:
            qs = City.objects.all()
        elif self.request.user.type == 2:
            qs = City.objects.filter(moderator=user_id)
        else:
            qs = None
        context.update({
            'city_list': qs
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
    context.update({
        'object': porch,
        'surface': porch.surface,
        'porch_form': form,
        'photo_form': photo_form
    })
    return render(request, 'surface/surface_porch_update.html', context)


def surface_photo_add(request):
    if request.method == 'POST':
        form = SurfacePhotoForm(request.POST, request.FILES)
        if form.is_valid():
            # file is saved
            instance = form.save()
            return HttpResponseRedirect(reverse('surface:porch-update', args=(instance.porch.id, )))
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def surface_photo_update(request, pk):
    context = {}
    photo = SurfacePhoto.objects.get(pk=int(pk))
    success_msg = u''
    error_msg = u''
    if request.method == 'POST':
        form = SurfacePhotoForm(request.POST, request.FILES, instance=photo)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('surface:porch', args=(photo.porch.id, )))
    else:
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
# def client_order(request, pk):
#     context = {}
#     client = Client.objects.get(pk=int(pk))
#     success_msg = u''
#     error_msg = u''
#     if request.method == 'POST':
#         form = ClientOrderForm(request.POST)
#         if form.is_valid():
#             order = form.save()
#             return HttpResponseRedirect(reverse('client:order-update', args=(order.id, )))
#     else:
#         form = ClientOrderForm(initial={
#             'client': client
#         })
#     context.update({
#         'success': success_msg,
#         'error': error_msg,
#         'client_order_form': form,
#         'object': client,
#         'client': client
#     })
#     return render(request, 'client/client_order.html', context)
