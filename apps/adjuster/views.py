# coding=utf-8
from datetime import datetime
from annoying.functions import get_object_or_None
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView
import xlwt
from apps.adjuster.forms import AdjusterAddForm, AdjusterUpdateForm, AdjusterPaymentForm
from apps.city.models import City
from apps.manager.models import Manager
from core.forms import UserAddForm, UserUpdateForm
from .models import Adjuster

__author__ = 'alexy'


class AdjusterListView(ListView):
    model = Adjuster
    paginate_by = 25

    def get_queryset(self):
        user = self.request.user
        if user.type == 1:
            qs = Adjuster.objects.select_related().all()
        elif user.type == 6:
            qs = Adjuster.objects.select_related().filter(city__in=user.superviser.city.all())
        elif user.type == 2:
            qs = Adjuster.objects.select_related().filter(city__moderator=user)
        elif user.type == 5:
            qs = Adjuster.objects.select_related().filter(city__moderator=user.manager.moderator)
        else:
            qs = None
        if self.request.GET.get('email'):
            qs = qs.filter(user__email__icontains=self.request.GET.get('email'))
        if self.request.GET.get('last_name'):
            qs = qs.filter(user__last_name__icontains=self.request.GET.get('last_name'))
        if self.request.GET.get('city') and int(self.request.GET.get('city')) != 0:
            qs = qs.filter(city__id=int(self.request.GET.get('city')))
        return qs

    def get_context_data(self, **kwargs):
        context = super(AdjusterListView, self).get_context_data()
        user = self.request.user
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
        context.update({
            'city_list': city_qs
        })
        if self.request.GET.get('city'):
            context.update({
                'city_id': int(self.request.GET.get('city'))
            })
        if self.request.GET.get('email'):
            context.update({
                'r_email': self.request.GET.get('email')
            })
        if self.request.GET.get('last_name'):
            context.update({
                'r_last_name': self.request.GET.get('last_name')
            })
        if self.request.META['QUERY_STRING']:
            self.request.session['adjuster_filtered_list'] = '%s?%s' % (self.request.path, self.request.META['QUERY_STRING'])
        else:
            self.request.session['adjuster_filtered_list'] = reverse('adjuster:list')
        return context


@login_required
def adjuster_add(request):
    context = {}
    if request.method == "POST":
        user_form = UserAddForm(request.POST)
        adjuster_form = AdjusterAddForm(request.POST, request=request)
        if user_form.is_valid() and adjuster_form.is_valid():
            # TODO: сделать отправку сообщения о регистрации на email
            user = user_form.save(commit=False)
            user.type = 4
            user.save()
            adjuster = adjuster_form.save(commit=False)
            adjuster.user = user
            adjuster.save()
            return HttpResponseRedirect(reverse('adjuster:change', args=(adjuster.id, )))
        else:
            context.update({
                'error': u'Проверьте правильность ввода полей'
            })
    else:
        user_form = UserAddForm()
        adjuster_form = AdjusterAddForm(request=request)
    try:
        request.session['adjuster_filtered_list']
    except:
        request.session['adjuster_filtered_list'] = reverse('adjuster:list')
    context.update({
        'user_form': user_form,
        'adjuster_form': adjuster_form,
        'back_to_list': request.session['adjuster_filtered_list']
    })
    return render(request, 'adjuster/adjuster_add.html', context)


@login_required
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
        user_form = UserUpdateForm(request.POST, instance=user)
        adjuster_form = AdjusterUpdateForm(request.POST, request=request, instance=adjuster)
        if user_form.is_valid() and adjuster_form.is_valid():
            user_form.save()
            adjuster_form.save()
            success_msg += u' Изменения успешно сохранены'
        else:
            error_msg = u'Проверьте правильность ввода полей!'
    else:
        user_form = UserUpdateForm(instance=user)
        adjuster_form = AdjusterUpdateForm(request=request, instance=adjuster)
    try:
        request.session['adjuster_filtered_list']
    except:
        request.session['adjuster_filtered_list'] = reverse('adjuster:list')
    context.update({
        'success': success_msg,
        'error': error_msg,
        'user_form': user_form,
        'adjuster_form': adjuster_form,
        'adjuster': adjuster,
        'back_to_list': request.session['adjuster_filtered_list']
    })
    return render(request, 'adjuster/adjuster_update.html', context)


@login_required
def adjuster_task(request, pk):
    context = {}
    r_date_s = request.GET.get('date_s')
    r_date_e = request.GET.get('date_e')
    context.update({
        'r_date_s': r_date_s,
        'r_date_e': r_date_e
    })
    adjuster = Adjuster.objects.get(pk=int(pk))
    qs = adjuster.adjustertask_set.all()
    if r_date_s:
        qs = qs.filter(date__gte=datetime.strptime(r_date_s, '%d.%m.%Y'))
    if r_date_e:
        qs = qs.filter(date__lte=datetime.strptime(r_date_e, '%d.%m.%Y'))
    total_sum = 0
    for i in qs:
        total_sum += i.get_actual_cost()
    paginator = Paginator(qs, 25)
    page = request.GET.get('page')
    try:
        task_list = paginator.page(page)
    except PageNotAnInteger:
        task_list = paginator.page(1)
    except EmptyPage:
        task_list = paginator.page(paginator.num_pages)
    try:
        request.session['adjuster_filtered_list']
    except:
        request.session['adjuster_filtered_list'] = reverse('adjuster:list')
    context.update({
        'adjuster': adjuster,
        'task_list': task_list,
        'total_sum': total_sum,
        'back_to_list': request.session['adjuster_filtered_list']
    })
    return render(request, 'adjuster/adjuster_task.html', context)


@login_required
def adjuster_payment(request, pk):
    adjuster = Adjuster.objects.get(pk=int(pk))
    context = {
        'adjuster': adjuster
    }
    if request.method == 'POST':
        form = AdjusterPaymentForm(request.POST, instance=adjuster)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adjuster:change', args=(adjuster.id, )))
    else:
        form = AdjusterPaymentForm(instance=adjuster)
    try:
        request.session['adjuster_filtered_list']
    except:
        request.session['adjuster_filtered_list'] = reverse('adjuster:list')
    context.update({
        'form': form,
        'back_to_list': request.session['adjuster_filtered_list']
    })
    return render(request, 'adjuster/adjuster_payment.html', context)


@login_required
def adjuster_report(request):
    context = {}
    user = request.user
    if user.type == 1:
        qs = Adjuster.objects.select_related().all()
        city_qs = City.objects.all()
    elif user.type == 6:
        qs = Adjuster.objects.select_related().filter(city__in=user.superviser.city_id_list())
        city_qs = user.superviser.city.all()
    elif user.type == 2:
        qs = Adjuster.objects.select_related().filter(city__moderator=user)
        city_qs = City.objects.filter(moderator=user)
    elif user.type == 5:
        qs = Adjuster.objects.select_related().filter(city__moderator=user.manager.moderator)
        city_qs = City.objects.filter(moderator=user.manager.moderator)
    else:
        qs = city_qs = None
    r_email = request.GET.get('email')
    r_last_name = request.GET.get('last_name')
    r_city = request.GET.get('city')
    r_date_s = request.GET.get('date_s')
    r_date_e = request.GET.get('date_e')
    if not r_email and not r_last_name and not r_city and not r_date_e and not r_date_s:
        qs = None
    context.update({
        'city_list': city_qs
    })

    context.update({
        'r_date_s': r_date_s,
        'r_date_e': r_date_e
    })
    if r_email:
        qs = qs.filter(user__email__icontains=r_email)
        context.update({
            'r_email': r_email
        })
    if r_last_name:
        qs = qs.filter(user__last_name__icontains=r_last_name)
        context.update({
            'r_last_name': r_last_name
        })
    if r_city and int(r_city) != 0:
        qs = qs.filter(city__id=int(r_city))
    try:
        context.update({
            'r_city': int(r_city)
        })
    except:
        pass
    if qs:
        for adjuster in qs:
            a_task_qs = adjuster.adjustertask_set.all()
            if r_date_s:
                a_task_qs = a_task_qs.filter(date__gte=datetime.strptime(r_date_s, '%d.%m.%Y'))
            if r_date_e:
                a_task_qs = a_task_qs.filter(date__lte=datetime.strptime(r_date_e, '%d.%m.%Y'))
            adjuster.task_count = a_task_qs.count()
            adjuster.stand_count = 0
            for item in a_task_qs:
                adjuster.stand_count += item.get_porch_count()
            adjuster.repair_count = 0
            for item in a_task_qs.filter(type=2):
                adjuster.repair_count += item.get_porch_count()
            adjuster.change_count = 0
            for item in a_task_qs.filter(type=1):
                adjuster.change_count += item.get_porch_count()
            adjuster.new_count = 0
            for item in a_task_qs.filter(type=0):
                adjuster.new_count += item.get_porch_count()
            adjuster.actual_cost = 0
            adjuster.total_cost = 0
            for item in a_task_qs:
                adjuster.actual_cost += item.get_actual_cost()
                adjuster.total_cost += item.get_total_cost()
    context.update({
        'object_list': qs
    })
    return render(request, 'adjuster/adjuster_report.html', context)


def adjuster_report_excel(request):
    """
    Экспорт отчёта по выбранным монтажникам в xls файл
    :param request:
    :return:
    """
    adjuster_qs = None
    date_from = request.POST.get('date_from')
    date_to = request.POST.get('date_to')
    if request.POST.getlist('chk_group[]'):
        adjuster_list = [int(i) for i in request.POST.getlist('chk_group[]')]
        adjuster_qs = Adjuster.objects.filter(pk__in=adjuster_list)
    font0 = xlwt.Font()
    font0.name = 'Calibri'
    font0.height = 220

    borders = xlwt.Borders()
    borders.left = xlwt.Borders.THIN
    borders.right = xlwt.Borders.THIN
    borders.top = xlwt.Borders.THIN
    borders.bottom = xlwt.Borders.THIN

    style0 = xlwt.XFStyle()
    style0.font = font0

    style1 = xlwt.XFStyle()
    style1.font = font0
    style1.borders = borders

    wb = xlwt.Workbook()
    ws = wb.add_sheet(u'Монтажники')
    ws.write(0, 0, u'Отчёт по монтажникам:', style0)
    ws.write(1, 0, u'Выбранный период:', style0)
    ws.write(1, 1, u'%s' % date_from, style0)
    ws.write(1, 2, u'%s' % date_to, style0)

    ws.write(3, 0, u'ФИО', style1)
    ws.write(3, 1, u'Город', style1)
    ws.write(3, 2, u'Задачи', style1)
    ws.write(3, 3, u'Поверхности', style1)
    ws.write(3, 4, u'Ремонт', style1)
    ws.write(3, 5, u'Замены', style1)
    ws.write(3, 6, u'Новые конструкции', style1)
    ws.write(3, 7, u'Стоимость работ', style1)
    ws.write(3, 8, u'Сумма к выплате', style1)
    total_task = total_stand = total_repair = total_change = total_new = total_cost = actual_cost = 0
    i = 4
    if adjuster_qs:
        for adjuster in adjuster_qs:
            a_task_qs = adjuster.adjustertask_set.all()
            if date_from:
                a_task_qs = a_task_qs.filter(date__gte=datetime.strptime(date_from, '%d.%m.%Y'))
            if date_to:
                a_task_qs = a_task_qs.filter(date__lte=datetime.strptime(date_to, '%d.%m.%Y'))
            adjuster.task_count = a_task_qs.count()
            adjuster.stand_count = 0
            for item in a_task_qs:
                adjuster.stand_count += item.get_porch_count()
            adjuster.repair_count = 0
            for item in a_task_qs.filter(type=2):
                adjuster.repair_count += item.get_porch_count()
            adjuster.change_count = 0
            for item in a_task_qs.filter(type=1):
                adjuster.change_count += item.get_porch_count()
            adjuster.new_count = 0
            for item in a_task_qs.filter(type=0):
                adjuster.new_count += item.get_porch_count()
            adjuster.actual_cost = 0
            adjuster.total_cost = 0
            for item in a_task_qs:
                adjuster.actual_cost += item.get_actual_cost()
                adjuster.total_cost += item.get_total_cost()
            total_task += adjuster.task_count
            total_stand += adjuster.stand_count
            total_repair += adjuster.repair_count
            total_change += adjuster.change_count
            total_new += adjuster.new_count
            total_cost += adjuster.total_cost
            actual_cost += adjuster.actual_cost

            ws.write(i, 0, adjuster.__unicode__(), style1)
            ws.write(i, 1, adjuster.city.name, style1)
            ws.write(i, 2, adjuster.task_count, style1)
            ws.write(i, 3, adjuster.stand_count, style1)
            ws.write(i, 4, adjuster.repair_count, style1)
            ws.write(i, 5, adjuster.change_count, style1)
            ws.write(i, 6, adjuster.new_count, style1)
            ws.write(i, 7, adjuster.total_cost, style1)
            ws.write(i, 8, adjuster.actual_cost, style1)
            i += 1
        ws.write(i, 0, u'Итого', style0)
        ws.write(i, 2, total_task, style0)
        ws.write(i, 3, total_stand, style0)
        ws.write(i, 4, total_repair, style0)
        ws.write(i, 5, total_change, style0)
        ws.write(i, 6, total_new, style0)
        ws.write(i, 7, total_cost, style0)
        ws.write(i, 8, actual_cost, style0)

    ws.col(0).width = 10000
    ws.col(1).width = 6000
    ws.col(2).width = 3000
    ws.col(3).width = 4000
    ws.col(4).width = 3000
    ws.col(5).width = 3000
    ws.col(6).width = 6500
    ws.col(7).width = 5100
    ws.col(8).width = 5100
    for count in range(i+1):
        ws.row(count).height = 400

    fname = 'adjuster_report.xls'
    response = HttpResponse(content_type="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=%s' % fname
    wb.save(response)
    return response


def adjuster_detail_report_excel(request, pk):
    """
    Экспорт детального отчёта по выбранному монтажнику в xls файл
    :param request:
    :return:
    """
    adjuster = get_object_or_None(Adjuster, pk=int(pk))
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    font0 = xlwt.Font()
    font0.name = 'Calibri'
    font0.height = 220

    borders = xlwt.Borders()
    borders.left = xlwt.Borders.THIN
    borders.right = xlwt.Borders.THIN
    borders.top = xlwt.Borders.THIN
    borders.bottom = xlwt.Borders.THIN

    style0 = xlwt.XFStyle()
    style0.font = font0

    style1 = xlwt.XFStyle()
    style1.font = font0
    style1.borders = borders

    wb = xlwt.Workbook()
    ws = wb.add_sheet(u'Отчёт')
    if adjuster:
        ws.write(0, 0, u'Отчёт по монтажнику:', style0)
        ws.write(0, 1, adjuster.__unicode__(), style0)

        ws.write(1, 0, u'Выбранный период:', style0)
        ws.write(1, 1, u'%s' % date_from or '', style0)
        ws.write(1, 2, u'%s' % date_to or '', style0)

        ws.write(3, 0, u'Дата', style1)
        ws.write(3, 1, u'Тип задачи', style1)
        ws.write(3, 2, u'Количество адресов', style1)
        ws.write(3, 3, u'Количество стендов', style1)
        ws.write(3, 4, u'Стоимость работ', style1)
        ws.write(3, 5, u'Сумма к выплате', style1)
        total_surface = total_stand = total_cost = actual_cost = 0
        i = 4
        a_task_qs = adjuster.adjustertask_set.all()
        if date_from:
            a_task_qs = a_task_qs.filter(date__gte=datetime.strptime(date_from, '%d.%m.%Y'))
        if date_to:
            a_task_qs = a_task_qs.filter(date__lte=datetime.strptime(date_to, '%d.%m.%Y'))
        for task in a_task_qs:
            total_surface += task.get_surface_count()
            total_stand += task.get_porch_count()
            total_cost += task.get_total_cost()
            actual_cost += task.get_actual_cost()

            ws.write(i, 0, task.date.strftime('%d.%m.%Y'), style1)
            ws.write(i, 1, task.get_type_display(), style1)
            ws.write(i, 2, task.get_surface_count(), style1)
            ws.write(i, 3, task.get_porch_count(), style1)
            ws.write(i, 4, task.get_total_cost(), style1)
            ws.write(i, 5, task.get_actual_cost(), style1)
            i += 1
        ws.write(i, 0, u'Итого', style0)
        ws.write(i, 1, a_task_qs.count(), style0)
        ws.write(i, 2, total_surface, style0)
        ws.write(i, 3, total_stand, style0)
        ws.write(i, 4, total_cost, style0)
        ws.write(i, 5, actual_cost, style0)

        ws.col(0).width = 10000
        ws.col(1).width = 10000
        ws.col(2).width = 6000
        ws.col(3).width = 6000
        ws.col(4).width = 6000
        ws.col(5).width = 6000
        for count in range(i+1):
            ws.row(count).height = 400

    fname = 'adjuster_detail_report.xls'
    response = HttpResponse(content_type="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=%s' % fname
    wb.save(response)
    return response
