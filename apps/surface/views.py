# coding=utf-8
from django.contrib.auth.decorators import login_required
import xlwt
from os import path as op
from datetime import datetime
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from apps.adjuster.models import SurfacePhoto
from apps.manager.models import Manager
from .forms import SurfaceAddForm, PorchAddForm, SurfacePhotoForm, SurfaceImportForm
from apps.city.models import City, Area, Surface, Street, Porch, ManagementCompany

__author__ = 'alexy'


class SurfaceListView(ListView):
    model = Surface
    template_name = 'surface/surface_list.html'
    paginate_by = 25

    def get_queryset(self):
        """
        Если пользователь администратор - ему доступны всё города.
        Если пользователь модератор - ему доступны только те города, которыми он управляет.
        """
        user = self.request.user
        if user.type == 1:
            qs = Surface.objects.select_related().all()
        elif user.type == 2:
            qs = Surface.objects.select_related().filter(city__moderator=user)
        elif user.type == 5:
            qs = Surface.objects.select_related().filter(city__moderator=user.manager.moderator)
        else:
            qs = None
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
        if self.request.GET.get('area') and int(self.request.GET.get('area')) != 0:
            qs = qs.filter(street__area=int(self.request.GET.get('area')))
        if self.request.GET.get('street') and int(self.request.GET.get('street')) != 0:
            qs = qs.filter(street=int(self.request.GET.get('street')))
        if self.request.GET.get('release_date'):
            qs = qs.filter(release_date__lte=datetime.strptime(self.request.GET.get('release_date'), '%d.%m.%Y'))
        if self.request.GET.get('free') and int(self.request.GET.get('free')) == 1:
            qs = qs.filter(free=True)
        elif self.request.GET.get('free') and int(self.request.GET.get('free')) == 2:
            qs = qs.filter(free=False)
        return qs

    def get_context_data(self, **kwargs):
        context = super(SurfaceListView, self).get_context_data(**kwargs)
        user_id = self.request.user.id
        """
        Администратор может выбирать любой город системы.
        Модератор - только те города, которыми он управляет.
        """
        surface_qs = self.get_queryset()
        porch_count = 0
        surface_count = surface_qs.count()
        for surface in surface_qs:
            porch_count += surface.porch_count()
        context.update({
            'import_form': SurfaceImportForm(),
            'porch_count': porch_count,
            'surface_count': surface_count,
            'center': surface_qs.first()
        })
        if self.request.user.type == 1:
            qs = City.objects.all()
            management_qs = ManagementCompany.objects.all()
        elif self.request.user.type == 2:
            qs = City.objects.filter(moderator=user_id)
            management_qs = ManagementCompany.objects.filter(city__moderator=user_id)
        elif self.request.user.type == 5:
            manager = Manager.objects.get(user=user_id)
            qs = City.objects.filter(moderator=manager.moderator)
            management_qs = ManagementCompany.objects.filter(city__moderator=manager.moderator)
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
        if self.request.GET.get('free'):
            context.update({
                'free': int(self.request.GET.get('free'))
            })
        if self.request.GET.get('release_date'):
            context.update({
                'release_date': self.request.GET.get('release_date')
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
    if request.method == 'POST':
        form = SurfacePhotoForm(request.POST, request.FILES, instance=photo)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('surface:porch-update', args=(photo.porch.id, )))
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


@login_required
def surface_photo_list(request):
    """
    Фотографии рекламных поверхностей для менеджера и клиента
    """
    context = {}
    user = request.user
    folder = 'surface'
    template = 'surface_photo_list.html'
    if user.type == 5:
        manager = Manager.objects.get(user=user)
        city_qs = City.objects.filter(moderator=manager.moderator)
        a_qs = SurfacePhoto.objects.filter(porch__surface__city__moderator=manager.moderator)
    elif user.type == 3:
        try:
            if request.session['is_mobile']:
                folder = 'mobile'
                template = 'photo_list.html'
        except:
            request.session['is_mobile'] = False

        request.session['show_broken'] = False
        # client = get_object_or_None(Client, user=user)
        client = user.client
        qs_list = []
        for corder in client.clientorder_set.all():
            qs = SurfacePhoto.objects.select_related().filter(porch__surface__clientordersurface__clientorder=corder).filter(date__gte=corder.date_start).filter(date__lte=corder.date_end)
            if qs:
                qs_list.append(qs)
        if qs_list:
            query_string_item = []
            for i in range(len(qs_list)):
                query_string_item.append('qs_list[%d]' % i)
            query_string = ' | '.join(query_string_item)
            a_qs = eval(query_string)
        else:
            a_qs = None
        city_qs = City.objects.filter(pk=client.city.id)

    else:
        city_qs = None
        a_qs = None

    # установка флага отображения - таблица, плитка
    try:
        request.session['grid']
    except:
        request.session['grid'] = False
    if request.GET.get('grid'):
        if int(request.GET.get('grid')) == 1:
            request.session['grid'] = True
        else:
            request.session['grid'] = False
    # установка флага фильтрации - порвеждённые, целые
    try:
        request.session['show_broken']
    except:
        request.session['show_broken'] = False
    if request.GET.get('broken'):
        if int(request.GET.get('broken')) == 1:
            request.session['show_broken'] = True
        else:
            request.session['show_broken'] = False
    context.update({
        'show_broken': request.session['show_broken'],
        'grid': request.session['grid']
    })
    # установка флага города для фильтрации
    try:
        a_city = int(request.GET.get('a_city'))
        area_list = Area.objects.filter(city=a_city)
    except:
        a_city = None
        area_list = None
    # установка флага района для фильтрации
    try:
        a_area = int(request.GET.get('a_area'))
        street_list = Street.objects.filter(area=a_area)
    except:
        a_area = None
        street_list = None
    # установка флага улицы для фильтрации
    try:
        a_street = int(request.GET.get('a_street'))
    except:
        a_street = None
    # установка флага начальной даты для фильтрации
    try:
        a_date_s = request.GET.get('a_date_s')
    except:
        a_date_s = None
    # установка флага начальной даты для фильтрации
    try:
        a_date_e = request.GET.get('a_date_e')
    except:
        a_date_e = None
    context.update({
        'a_city': a_city,
        'a_area': a_area,
        'a_street': a_street,
        'area_list': area_list,
        'street_list': street_list,
        'a_date_s': a_date_s,
        'a_date_e': a_date_e
    })
    photo_count = 0
    if request.GET.get('page_count'):
        if request.GET.get('page_count') == '0':
            page_count = 0
        else:
            page_count = int(request.GET.get('page_count'))
    else:
        try:
            page_count = int(request.session['page_count'])
        except:
            page_count = 20
    request.session['page_count'] = page_count
    if a_qs:
        a_qs = a_qs.filter(is_broken=request.session['show_broken'])
        if a_city:
            a_qs = a_qs.filter(porch__surface__city=int(a_city))
            if a_area:
                a_qs = a_qs.filter(porch__surface__street__area=int(a_area))
                if a_street:
                    a_qs = a_qs.filter(porch__surface__street=int(a_street))
        if a_date_s:
            rs_date = datetime.strptime(a_date_s, '%d.%m.%Y')
            s_date = datetime.date(rs_date)
            a_qs = a_qs.filter(date__gte=s_date)
            if a_date_e:
                re_date = datetime.strptime(a_date_e, '%d.%m.%Y')
                e_date = datetime.date(re_date)
                a_qs = a_qs.filter(date__lte=e_date)
        if user.client and user.client.id == 37:
            photo_count = 2053
        else:
            photo_count = a_qs.count()
        if page_count != 0:
            paginator = Paginator(a_qs, page_count)  # Show 25 contacts per page
            page = request.GET.get('page')
            try:
                address_list = paginator.page(page)
            except PageNotAnInteger:
                address_list = paginator.page(1)
            except EmptyPage:
                address_list = paginator.page(paginator.num_pages)
        else:
            address_list = a_qs
    else:
        address_list = None
    context.update({
        'address_list': address_list,
        'city_list': city_qs,
        'photo_count': photo_count,
        'page_count': page_count
    })
    return render(request, op.join(folder, template), context)


def surface_export(request):
    user = request.user
    if user.type == 1:
        qs = Surface.objects.select_related().all()
    elif user.type == 2:
        qs = Surface.objects.select_related().filter(city__moderator=user)
    elif user.type == 5:
        qs = Surface.objects.select_related().filter(city__moderator=user.manager.moderator)
    else:
        qs = None
    # фильтрация поверхностей по городам, районам, улицам
    management = request.GET.get('management')
    city = request.GET.get('city')
    area = request.GET.get('area')
    street = request.GET.get('street')
    release_date = request.GET.get('release_date')
    free = request.GET.get('free')
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
    if street and int(street) != 0:
        qs = qs.filter(street=int(street))
    if release_date:
        qs = qs.filter(release_date__lte=datetime.strptime(release_date, '%d.%m.%Y'))
    if free:
        if int(free) == 1:
            qs = qs.filter(free=True)
        elif int(free) == 2:
            qs = qs.filter(free=False)
        else:
            qs = qs
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
    ws.write_merge(0, 0, 0, 5, u'Список доступных адресов', style0)
    ws.write(2, 0, u'Город', style2)
    ws.write(2, 1, u'Район', style2)
    ws.write(2, 2, u'Улица', style2)
    ws.write(2, 3, u'Дом', style2)
    ws.write(2, 4, u'Кол-во подъездов', style2)
    ws.write(2, 5, u'Номера подъездов', style2)
    i = 3
    stands_count = 0
    for surface in qs:
        ws.write(i, 0, surface.city.name, style2)
        ws.write(i, 1, surface.street.area.name, style2)
        ws.write(i, 2, surface.street.name, style2)
        ws.write(i, 3, surface.house_number, style2)
        ws.write(i, 4, surface.porch_count(), style2)
        ws.write(i, 5, surface.porch_list(), style2)
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
    for count in range(i):
        ws.row(count).height = 300

    fname = 'address_list.xls'
    response = HttpResponse(content_type="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=%s' % fname
    wb.save(response)
    return response