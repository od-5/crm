# coding=utf-8
import os
import uuid
import zipfile
from io import BytesIO

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
import xlwt
from os import path as op
import datetime
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from docxtpl import DocxTemplate

from apps.adjuster.models import SurfacePhoto
from apps.client.models import Client, ClientOrderSurface
from apps.manager.models import Manager
from lib.cbv import DocResponseMixin
from .forms import SurfaceAddForm, PorchAddForm, SurfacePhotoForm, SurfaceImportForm
from apps.city.models import City, Area, Surface, Street, Porch, ManagementCompany, SurfaceDocTemplate

__author__ = 'alexy'


class SurfaceListView(ListView):
    model = Surface
    template_name = 'surface/surface_list.html'
    paginate_by = 25

    def get_paginate_by(self, queryset):
        """
        Получение параметра - сколько показывать элементов на странице
        """
        if self.request.GET.get('page_count'):
            if self.request.GET.get('page_count') == '0':
                page_count = 0
            else:
                page_count = int(self.request.GET.get('page_count'))
        else:
            try:
                page_count = int(self.request.session['page_count'])
            except:
                page_count = self.paginate_by
        self.paginate_by = self.request.session['page_count'] = page_count
        return page_count

    def get_qs(self):
        user = self.request.user
        if user.type == 1:
            qs = Surface.objects.select_related('city', 'street', 'street__city', 'street__area', 'management').all()
        elif user.type == 6:
            qs = Surface.objects.select_related('city', 'street', 'street__area', 'management').filter(
                city__in=user.superviser.city_id_list())
        elif user.type == 2:
            qs = Surface.objects.select_related('city', 'street', 'street__area', 'management').filter(
                city__moderator=user)
        elif user.type == 5:
            qs = Surface.objects.select_related('city', 'street', 'street__area', 'management').filter(
                city__moderator=user.manager.moderator)
        else:
            qs = Surface.objects.none()
        return qs.prefetch_related('porch_set', 'street__city__street_set', 'clientordersurface_set__clientorder')

    def get_queryset(self):
        """
        Если пользователь администратор - ему доступны всё города.
        Если пользователь модератор - ему доступны только те города, которыми он управляет.
        """
        user = self.request.user
        qs = self.get_qs()
        # фильтрация поверхностей по городам, районам, улицам
        if self.request.GET.get('management'):
            if int(self.request.GET.get('management')) == 0:
                qs = qs
            elif int(self.request.GET.get('management')) == -1:
                qs = qs.filter(management__isnull=True)
            else:
                qs = qs.filter(management=int(self.request.GET.get('management')))
        if self.request.GET.get('city') and int(self.request.GET.get('city')) != 0:
            qs = qs.filter(city=int(self.request.GET.get('city')))
        else:
            qs = qs.none()
        if self.request.GET.get('area') and int(self.request.GET.get('area')) != 0:
            qs = qs.filter(street__area=int(self.request.GET.get('area')))
        if self.request.GET.get('street') and self.request.GET.get('street') != '':
            qs = qs.filter(street__name__icontains=self.request.GET.get('street'))
        if self.request.GET.get('release_date'):
            if self.request.GET.get('free') and int(self.request.GET.get('free')) == 2:
                qs = qs.filter(release_date__gte=datetime.datetime.strptime(self.request.GET.get('release_date'), '%d.%m.%Y'))
            else:
                qs = qs.filter(release_date__lt=datetime.datetime.strptime(self.request.GET.get('release_date'), '%d.%m.%Y'))
        if self.request.GET.get('free') and not self.request.GET.get('release_date'):
            if int(self.request.GET.get('free')) == 1:
                qs = qs.filter(free=True)
            if int(self.request.GET.get('free')) == 2:
                qs = qs.filter(free=False)
        if self.request.GET.get('has_stand') and int(self.request.GET.get('has_stand')) == 1:
            qs = qs.filter(has_stand=True)
        elif self.request.GET.get('has_stand') and int(self.request.GET.get('has_stand')) == 2:
            qs = qs.filter(has_stand=False)
        if self.request.GET.get('client') and int(self.request.GET.get('client')) != 0:
            today = datetime.datetime.today()
            client_filter = ClientOrderSurface.objects.filter(
                surface__in=qs,
                clientorder__date_end__gte=today,
                clientorder__client=int(self.request.GET.get('client'))
            ).values_list('surface', flat=True)
            qs = qs.filter(id__in=client_filter)
        return qs.order_by('street__area', 'street__name', 'house_number')

    def get_context_data(self, **kwargs):
        context = super(SurfaceListView, self).get_context_data(**kwargs)
        user = self.request.user
        """
        Администратор может выбирать любой город системы.
        Модератор - только те города, которыми он управляет.
        """
        surface_qs = self.object_list
        try:
            porch_count = surface_qs.aggregate(Sum('porch_total_count'))['porch_total_count__sum']
        except:
            porch_count = 0
        surface_count = surface_qs.count()
        # for surface in surface_qs:
        #     porch_count += surface.porch_count()
        today = datetime.datetime.today()
        client_qs = Client.objects.filter(
            clientorder__clientordersurface__surface__in=self.get_qs(),
            clientorder__date_end__gte=today
        ).distinct()
        if self.request.GET.get('city'):
            client_qs = client_qs.filter(city_id=self.request.GET.get('city'))
        context.update({
            'import_form': SurfaceImportForm(),
            'porch_count': porch_count,
            'surface_count': surface_count,
            'center': surface_qs.first(),
            'client_list': client_qs.values('id', 'legal_name'),
            'page_count': self.paginate_by,
        })
        if user.type == 1:
            qs = City.objects.all()
            management_qs = ManagementCompany.objects.all()
        elif user.type == 6:
            qs = user.superviser.city.all()
            management_qs = ManagementCompany.objects.filter(city__in=user.superviser.city_id_list())
        elif user.type == 2:
            qs = City.objects.filter(moderator=user)
            management_qs = ManagementCompany.objects.filter(city__moderator=user)
        elif user.type == 5:
            qs = City.objects.filter(moderator=user.manager.moderator)
            management_qs = ManagementCompany.objects.filter(city__moderator=user.manager.moderator)
        else:
            qs = None
            management_qs = None

        if self.request.GET.get('city'):
            management_qs = management_qs.filter(city_id=self.request.GET.get('city'))

        context.update({
            'city_list': qs,
            'management_list': management_qs
        })

        if self.request.GET.get('client'):
            context.update({
                'client_id': int(self.request.GET.get('client'))
            })

        if self.request.GET.get('city'):
            area_qs = Area.objects.filter(city__id=int(self.request.GET.get('city')))
            context.update({
                'area_list': area_qs,
                'city_id': int(self.request.GET.get('city'))
            })
            if self.request.GET.get('area'):
                context.update({
                    'area_id': int(self.request.GET.get('area'))
                })
                if self.request.GET.get('street'):
                    context.update({
                        'street': self.request.GET.get('street')
                    })
        if self.request.GET.get('management'):
            context.update({
                'management_id': int(self.request.GET.get('management'))
            })
        if self.request.GET.get('free'):
            context.update({
                'free': int(self.request.GET.get('free'))
            })
        if self.request.GET.get('has_stand'):
            context.update({
                'has_stand': int(self.request.GET.get('has_stand'))
            })
        if self.request.GET.get('release_date'):
            context.update({
                'release_date': self.request.GET.get('release_date')
            })
        if self.request.META['QUERY_STRING']:
            self.request.session['surface_filtered_list'] = '%s?%s' % (self.request.path, self.request.META['QUERY_STRING'])
        else:
            self.request.session['surface_filtered_list'] = reverse('surface:list')
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
        initial = initial.copy()
        initial['user'] = self.request.user
        return initial

    def get_context_data(self, **kwargs):
        context = super(SurfaceCreateView, self).get_context_data(**kwargs)
        try:
            self.request.session['surface_filtered_list']
        except:
            self.request.session['surface_filtered_list'] = reverse('surface:list')
        context.update({
            'back_to_list': self.request.session['surface_filtered_list']
        })
        return context


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
        initial = initial.copy()
        initial['user'] = self.request.user
        return initial

    def get_context_data(self, **kwargs):
        context = super(SurfaceUpdateView, self).get_context_data(**kwargs)
        try:
            self.request.session['surface_filtered_list']
        except:
            self.request.session['surface_filtered_list'] = reverse('surface:list')
        context.update({
            'surface': self.object,
            'back_to_list': self.request.session['surface_filtered_list']
        })
        return context


class SurfacePhotoDeleteView(DeleteView):
    model = SurfacePhoto
    template_name = 'surface/surface_photo_delete.html'
    success_url = '/surface/'

    def get_context_data(self, **kwargs):
        context = super(SurfacePhotoDeleteView, self).get_context_data(**kwargs)
        try:
            self.request.session['surface_filtered_list']
        except:
            self.request.session['surface_filtered_list'] = reverse('surface:list')
        context.update({
            'surface': self.object.porch.surface,
            'back_to_list': self.request.session['surface_filtered_list']
        })
        return context


class PorchView(CreateView):
    model = Porch
    template_name = 'surface/surface_porch.html'
    form_class = PorchAddForm

    def get_initial(self):
        surface = get_object_or_404(Surface, pk=int(self.kwargs.get('pk')))
        return {
            'surface': surface
        }

    def get_context_data(self, **kwargs):
        context = super(PorchView, self).get_context_data(**kwargs)
        try:
            self.request.session['surface_filtered_list']
        except:
            self.request.session['surface_filtered_list'] = reverse_lazy('surface:list')
        surface = get_object_or_404(Surface, pk=int(self.kwargs.get('pk')))
        context.update({
            'back_to_list': self.request.session['surface_filtered_list'],
            'surface': surface
        })
        return context

    def get_success_url(self):
        return reverse_lazy('surface:porch', args=(self.object.surface.id, ))


@login_required
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
        'photo_form': photo_form,
        'back_to_list': reverse('surface:photo-list')
    })
    return render(request, 'surface/surface_porch_update.html', context)


@login_required
def surface_photo_add(request):
    if request.method == 'POST':
        form = SurfacePhotoForm(request.POST, request.FILES)
        if form.is_valid():
            date = form.cleaned_data['date']
            porch = form.cleaned_data['porch']
            tz = porch.surface.city.timezone
            time = datetime.datetime.combine(date.date(), datetime.datetime.now().time()) + \
                   datetime.timedelta(hours=tz)
            instance = form.save(commit=False)
            instance.date = time
            instance.save()
            return HttpResponseRedirect(reverse('surface:porch-update', args=(instance.porch.id, )))
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def surface_photo_update(request, pk):
    context = {}
    photo = SurfacePhoto.objects.get(pk=int(pk))
    success_msg = u''
    error_msg = u''
    if request.method == 'POST':
        form = SurfacePhotoForm(request.POST, request.FILES, instance=photo)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('surface:porch-update', args=(photo.porch.id, )))
    else:
        form = SurfacePhotoForm(instance=photo, initial={
            'file': photo.image.file
        })
    try:
        request.session['surface_filtered_list']
    except:
        request.session['surface_filtered_list'] = reverse('surface:list')
    context.update({
        'success': success_msg,
        'error': error_msg,
        'photo_form': form,
        'object': photo,
        'surface': photo.porch.surface,
        'back_to_list': request.session['surface_filtered_list']
    })
    return render(request, 'surface/surface_photo_update.html', context)


class SurfacePhotoListView(ListView):
    """
    Отображение списка фотографий
    """
    model = SurfacePhoto
    template_name = 'surface/surface_photo_list.html'
    paginate_by = 20
    context_object_name = 'address_list'

    # def get_template_names(self):
    #     """
    #     Выбор шаблона в зависимости от уровня доступа
    #     """
    #     folder = 'surface'
    #     template = 'surface_photo_list.html'
    #     if self.request.user.type == 3:
    #         try:
    #             if self.request.session['is_mobile']:
    #                 folder = 'mobile'
    #                 template = 'photo_list.html'
    #         except:
    #             self.request.session['is_mobile'] = False
    #     return op.join(folder, template)

    def get_paginate_by(self, queryset):
        """
        Получение параметра - сколько показывать элементов на странице
        """
        if self.request.GET.get('page_count'):
            if self.request.GET.get('page_count') == '0':
                page_count = 0
            else:
                page_count = int(self.request.GET.get('page_count'))
        else:
            try:
                page_count = int(self.request.session['page_count'])
            except:
                page_count = self.paginate_by
        self.paginate_by = self.request.session['page_count'] = page_count
        return page_count

    def get_queryset(self):
        """
        Получение queryset в зависимости от уровня доступа
        """
        user = self.request.user
        if user.type == 1:
            a_qs = SurfacePhoto.objects.select_related().all()
        elif user.type == 6:
            a_qs = SurfacePhoto.objects.select_related().filter(porch__surface__city__in=user.superviser.city_id_list())
        elif user.type == 2:
            a_qs = SurfacePhoto.objects.select_related().filter(porch__surface__city__moderator=user)
        elif user.type == 5:
            a_qs = SurfacePhoto.objects.filter(porch__surface__city__moderator=user.manager.moderator)
        elif user.type == 3:
            """
            Клиент может видеть только те фотографии, поверхности которых входят в его заказы, и дата фотографии
            находится в границах дат размещения заказа.
            """
            client = user.client
            qs_list = []
            for corder in client.clientorder_set.all():
                qs = SurfacePhoto.objects.select_related().filter(
                    porch__surface__clientordersurface__clientorder=corder).filter(
                    date__gte=corder.date_start).filter(date__lte=corder.date_end)
                if qs:
                    qs_list.append(qs)
            if qs_list:
                query_string_item = []
                for i in range(len(qs_list)):
                    query_string_item.append('qs_list[%d]' % i)
                query_string = ' | '.join(query_string_item)
                a_qs = eval(query_string)
            else:
                a_qs = self.model.objects.none()
        else:
            a_qs = self.model.objects.none()
        a_qs = a_qs.filter(is_broken=self.show_broken())
        filter_args = self.get_filter_args()
        if self.show_broken():
            if filter_args['broken_type']:
                filter_kwargs = {'porch__%s' % filter_args['broken_type']: True}
                a_qs = a_qs.filter(**filter_kwargs)
        if filter_args['a_city']:
            a_qs = a_qs.filter(porch__surface__city=filter_args['a_city'])
        else:
            a_qs = a_qs.none()
        if filter_args['a_area']:
            a_qs = a_qs.filter(porch__surface__street__area=filter_args['a_area'])
        if filter_args['a_street']:
            a_qs = a_qs.filter(porch__surface__street=filter_args['a_street'])
        if filter_args['a_house_number']:
            a_qs = a_qs.filter(porch__surface__house_number=filter_args['a_house_number'])
        if filter_args['a_date_s']:
            a_qs = a_qs.filter(date__gte=datetime.datetime.strptime(filter_args['a_date_s'], '%d.%m.%Y'))
        if filter_args['a_date_e']:
            a_qs = a_qs.filter(date__lte=datetime.datetime.strptime(filter_args['a_date_e'], '%d.%m.%Y'))
        return a_qs.select_related('porch', 'porch__surface', 'porch__surface__street',
                                   'porch__surface__street__area', 'porch__surface__city', 'adjuster',
                                   'adjuster__user')

    def grid_display(self):
        """
        установка флага отображения - таблица, плитка
        """
        try:
            self.request.session['grid']
        except:
            self.request.session['grid'] = False
        if self.request.GET.get('grid'):
            if int(self.request.GET.get('grid')) == 1:
                self.request.session['grid'] = True
            else:
                self.request.session['grid'] = False
        return self.request.session['grid']

    def show_broken(self):
        """
        установка флага фильтрации - порвеждённые, целые
        """
        try:
            self.request.session['show_broken']
        except:
            self.request.session['show_broken'] = False
        if self.request.GET.get('broken'):
            if int(self.request.GET.get('broken')) == 1:
                self.request.session['show_broken'] = True
            else:
                self.request.session['show_broken'] = False
        return self.request.session['show_broken']

    def get_filter_args(self):
        """
        Подготовка данных для формы поиска и фильтрации queryset
        """
        a_city = a_area = a_street = area_list = street_list = broken_type = a_house_number = None
        if self.request.GET.get('a_city') and self.request.GET.get('a_city').isdigit():
            a_city = int(self.request.GET.get('a_city'))
            area_list = Area.objects.filter(city=a_city)
        if self.request.GET.get('a_area') and self.request.GET.get('a_area').isdigit():
            a_area = int(self.request.GET.get('a_area'))
            street_list = Street.objects.filter(area=a_area)
        if self.request.GET.get('a_street') and self.request.GET.get('a_street').isdigit():
            a_street = int(self.request.GET.get('a_street'))
        if self.request.GET.get('broken_type'):
            broken_type = self.request.GET.get('broken_type')
        if self.request.GET.get('a_house_number'):
            a_house_number = self.request.GET.get('a_house_number')
        a_date_s = self.request.GET.get('a_date_s') or None
        # установка флага начальной даты для фильтрации
        a_date_e = self.request.GET.get('a_date_e') or None
        return {
            'a_city': a_city,
            'a_area': a_area,
            'a_street': a_street,
            'a_date_s': a_date_s,
            'a_date_e': a_date_e,
            'area_list': area_list,
            'street_list': street_list,
            'broken_type': broken_type,
            'a_house_number': a_house_number
        }

    def get_context_data(self, **kwargs):
        context = super(SurfacePhotoListView, self).get_context_data(**kwargs)
        user = self.request.user
        photo_count = self.object_list.count()
        if user.type == 3 and user.client.photo_additional and photo_count > 0:
            photo_additional = user.client.photo_additional
            photo_count += photo_additional
        context.update({
            'photo_count': photo_count,
            'new': True,
            'page_count': self.paginate_by,
            'city_list': City.objects.get_qs(user),
            'grid': self.grid_display(),
            'show_broken': self.show_broken()
        })
        context.update(self.get_filter_args())
        return context


class SurfacePhotoZipView(SurfacePhotoListView):
    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        o = BytesIO()
        zip_file = zipfile.ZipFile(o, mode='w')
        for photo in qs:
            if photo.image_exists():
                zip_file.write(photo.image.path, photo.image.name.split('/')[-1])

        zip_file.close()

        o.seek(0)
        response = HttpResponse(o.getvalue())
        o.close()
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = "attachment; filename=\"photos.zip\""
        return response


def surface_export(request):
    user = request.user
    if user.type == 1:
        qs = Surface.objects.select_related('city', 'street', 'street__area', 'management').all()
    elif user.type == 6:
        qs = Surface.objects.select_related('city', 'street', 'street__area', 'management').filter(
            city__in=user.superviser.city_id_list())
    elif user.type == 2:
        qs = Surface.objects.select_related('city', 'street', 'street__area', 'management').filter(
            city__moderator=user)
    elif user.type == 5:
        qs = Surface.objects.select_related('city', 'street', 'street__area', 'management').filter(
            city__moderator=user.manager.moderator)
    else:
        qs = None
    # фильтрация поверхностей по городам, районам, улицам
    management = request.GET.get('management')
    city = request.GET.get('city')
    area = request.GET.get('area')
    street = request.GET.get('street')
    release_date = request.GET.get('release_date')
    free = request.GET.get('free')
    has_stand = request.GET.get('has_stand')
    if management:
        if int(management) == 0:
            qs = qs
        elif int(management) == -1:
            qs = qs.filter(management__isnull=True)
        else:
            qs = qs.filter(management=int(management))
    if city and int(city) != 0:
        qs = qs.filter(city=int(city))
    if area and int(area) != 0:
        qs = qs.filter(street__area=int(area))
    if street:
        qs = qs.filter(street__name__icontains=street)
    if free:
        if int(free) == 1:
            if release_date:
                qs = qs.filter(
                    release_date__lt=datetime.datetime.strptime(release_date, '%d.%m.%Y')
                )
            else:
                qs = qs.filter(free=True)
        elif int(free) == 2:
            if release_date:
                qs = qs.filter(
                    release_date__gt=datetime.datetime.strptime(release_date, '%d.%m.%Y')
                )
            else:
                qs = qs.filter(free=False)
    if has_stand:
        if int(has_stand) == 1:
            qs = qs.filter(has_stand=True)
        elif int(has_stand) == 2:
            qs = qs.filter(has_stand=False)
    if request.GET.get('client') and int(request.GET.get('client')) != 0:
        today = datetime.datetime.today()
        client_filter = ClientOrderSurface.objects.filter(
            surface__in=qs,
            clientorder__date_end__gte=today,
            clientorder__client=int(request.GET.get('client'))
        ).values_list('surface', flat=True)
        qs = qs.filter(id__in=client_filter)

    qs = qs.order_by('street__area', 'street__name', 'house_number')

    # выгрузка в excel
    font0 = xlwt.Font()
    font0.name = 'Times New Roman'
    font0.height = 240

    alignment_center = xlwt.Alignment()
    alignment_center.horz = xlwt.Alignment.HORZ_CENTER
    alignment_center.vert = xlwt.Alignment.VERT_TOP

    alignment_left = xlwt.Alignment()
    alignment_left.horz = xlwt.Alignment.HORZ_LEFT
    alignment_left.vert = xlwt.Alignment.VERT_TOP

    borders = xlwt.Borders()
    borders.left = xlwt.Borders.THIN
    borders.right = xlwt.Borders.THIN
    borders.top = xlwt.Borders.THIN
    borders.bottom = xlwt.Borders.THIN

    style0 = xlwt.XFStyle()
    style0.font = font0
    style0.alignment = alignment_center

    style1 = xlwt.XFStyle()
    style1.font = font0

    style2 = xlwt.XFStyle()
    style2.font = font0
    style2.borders = borders
    style2.alignment = alignment_left

    wb = xlwt.Workbook()
    ws = wb.add_sheet(u'Список адресов')
    ws.write_merge(0, 0, 0, 7, u'Список доступных адресов', style0)
    ws.write(2, 0, u'Город', style2)
    ws.write(2, 1, u'Район', style2)
    ws.write(2, 2, u'Улица', style2)
    ws.write(2, 3, u'Дом', style2)
    ws.write(2, 4, u'Кол-во подъездов', style2)
    ws.write(2, 5, u'Номера подъездов', style2)
    ws.write(2, 6, u'Клиент', style2)
    ws.write(2, 7, u'УК', style2)
    ws.write(2, 8, u'Этажей', style2)
    ws.write(2, 9, u'Квартир', style2)
    i = 3
    stands_count = 0
    for surface in qs:
        ws.write(i, 0, surface.city.name, style2)
        ws.write(i, 1, surface.street.area.name, style2)
        ws.write(i, 2, surface.street.name, style2)
        ws.write(i, 3, surface.house_number, style2)
        ws.write(i, 4, surface.porch_count(), style2)
        ws.write(i, 5, surface.porch_list(), style2)
        ws.write(i, 6, surface.get_current_client() or u'отсутствует', style2)
        ws.write(i, 7, surface.management.name if surface.management else u'не указана', style2)
        ws.write(i, 8, surface.floors, style2)
        ws.write(i, 9, surface.apart_count, style2)
        i += 1
        if surface.porch_count():
            stands_count += surface.porch_count()
    ws.write(i+1, 0, u'Итого стендов: %s' % stands_count,  style1)
    ws.col(0).width = 8000
    ws.col(1).width = 8000
    ws.col(2).width = 10000
    ws.col(3).width = 5000
    ws.col(4).width = 5000
    ws.col(5).width = 5000
    ws.col(6).width = 5000
    ws.col(7).width = 5000
    for count in range(i):
        ws.row(count).height = 300

    fname = 'address_list.xls'
    response = HttpResponse(content_type="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=%s' % fname
    wb.save(response)
    return response


class SurfaceDocView(DocResponseMixin, ListView):
    model = Porch
    template_name = 'surface.docx'
    filename = 'surface'

    def get_queryset(self):
        user = self.request.user
        if user.type == 1:
            qs = Surface.objects.select_related('city', 'street', 'street__area', 'management').all()
        elif user.type == 6:
            qs = Surface.objects.select_related('city', 'street', 'street__area', 'management').filter(
                city__in=user.superviser.city_id_list())
        elif user.type == 2:
            qs = Surface.objects.select_related('city', 'street', 'street__area', 'management').filter(
                city__moderator=user)
        elif user.type == 5:
            qs = Surface.objects.select_related('city', 'street', 'street__area', 'management').filter(
                city__moderator=user.manager.moderator)
        else:
            qs = None
        # фильтрация поверхностей по городам, районам, улицам
        management = self.request.GET.get('management')
        city = self.request.GET.get('city')
        area = self.request.GET.get('area')
        street = self.request.GET.get('street')
        release_date = self.request.GET.get('release_date')
        free = self.request.GET.get('free')
        has_stand = self.request.GET.get('has_stand')
        if management:
            if int(management) == 0:
                qs = qs
            elif int(management) == -1:
                qs = qs.filter(management__isnull=True)
            else:
                qs = qs.filter(management=int(management))
        if city and int(city) != 0:
            qs = qs.filter(city=int(city))
        if area and int(area) != 0:
            qs = qs.filter(street__area=int(area))
        if street:
            qs = qs.filter(street__name__icontains=street)
        if free:
            if int(free) == 1:
                if release_date:
                    qs = qs.filter(
                        release_date__lt=datetime.datetime.strptime(release_date, '%d.%m.%Y')
                    )
                else:
                    qs = qs.filter(free=True)
            elif int(free) == 2:
                if release_date:
                    qs = qs.filter(
                        release_date__gt=datetime.datetime.strptime(release_date, '%d.%m.%Y')
                    )
                else:
                    qs = qs.filter(free=False)
        if has_stand:
            if int(has_stand) == 1:
                qs = qs.filter(has_stand=True)
            elif int(has_stand) == 2:
                qs = qs.filter(has_stand=False)
        if self.request.GET.get('client') and int(self.request.GET.get('client')) != 0:
            today = datetime.datetime.today()
            client_filter = ClientOrderSurface.objects.filter(
                surface__in=qs,
                clientorder__date_end__gte=today,
                clientorder__client=int(self.request.GET.get('client'))
            ).values_list('surface', flat=True)
            qs = qs.filter(id__in=client_filter)
        return self.model.objects.filter(surface__in=qs).select_related(
            'surface', 'surface__street', 'surface__management'
        ).order_by('surface', 'number')


class SurfaceDocViewWithFile(SurfaceDocView):
    def get_document(self):
        uploaded_file = self.request.FILES.get('template')
        if not uploaded_file:
            return None
        if uploaded_file.content_type != 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            return None
        docx_model, created = SurfaceDocTemplate.objects.get_or_create()
        try:
            docx_model.docx.save(uploaded_file.name, uploaded_file)
        except UnicodeEncodeError:
            docx_model.docx.save('file#%s' % uuid.uuid4().hex[:8], uploaded_file)
        path = os.path.join(settings.BASE_DIR, '../../%s' % docx_model.docx.url)
        docx = DocxTemplate(path)
        return docx

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


@login_required
def update_company(request):
    surfaces = request.POST.getlist('chk_group[]')
    surface_qs = Surface.objects.filter(pk__in=surfaces)
    type = request.POST.get('type')
    if int(type) == 0:
        surface_qs.update(has_stand=True)
    if int(type) == 1:
        surface_qs.update(has_stand=False)
    if int(type) == 2:
        company = request.POST.get('company')
        surface_qs.update(management_id=company)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('surface:list')))
