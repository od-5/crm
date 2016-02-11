# coding=utf-8
from annoying.decorators import ajax_request
from apps.adjuster.models import Adjuster
from apps.city.forms import AreaAddForm, StreetForm
from apps.city.models import Area, City, Street, Surface, Porch
from apps.client.models import Client, ClientOrder
from apps.surface.forms import PorchAddForm
from core.models import User

__author__ = 'alexy'


@ajax_request
def get_city_area(request):
    if request.GET.get('city'):
        area_list = []
        area_qs = City.objects.get(pk=int(request.GET.get('city'))).area_set.all()
        print area_qs
        for i in area_qs:
            area_list.append({
                'id': i.id,
                'name': i.name
            })
        return {
            'area_list': area_list
        }
    else:
        return {
            'error': True
        }


@ajax_request
def simple_get_area_streets(request):
    if request.GET.get('area'):
        street_list = []
        area_pk = int(request.GET.get('area'))

        street_qs = Street.objects.filter(area=area_pk)
        print street_qs
        for street in street_qs:
            # if surface.id not in client_surfaces:
            street_list.append({
                'id': street.id,
                'name': street.name,
            })
        return {
            'street_list': street_list
        }
    else:
        return {
            'error': u'Что то пошло не так!'
        }



@ajax_request
def get_free_area_surface(request):
    if request.GET.get('area') and request.GET.get('order'):
        surface_list = []
        area_pk = int(request.GET.get('area'))
        order = ClientOrder.objects.get(pk=int(request.GET.get('order')))
        print u'дата начала размещения по заказу %s' % order.date_start
        surface_qs = Surface.objects.filter(street__area=area_pk, release_date__lt=order.date_start)
        for surface in surface_qs:
            if surface.id:
                surface_list.append({
                    'id': surface.id,
                    'street': surface.street.name,
                    'number': surface.house_number
                })
        return {
            'surface_list': surface_list
        }
    else:
        return {
            'error': u'Что то пошло не так!'
        }


@ajax_request
def surface_ajax(request):
    street_list = []
    if request.GET.get('city'):
        if int(request.GET.get('city')) == 0:
            user = User.objects.get(id=int(request.user.id))
            if user.type == 1:
                city = City.objects.all()
                street_qs = Street.objects.all()
            else:
                city = user.city_set.all()
                street_qs = Street.objects.filter(city__moderator=user)
        else:
            city = City.objects.get(id=int(request.GET.get('city')))
            street_qs = city.street_set.all()
        for i in street_qs:
            street_list.append(
                {
                    'id': i.id,
                    'name': i.name
                }
            )
        return {
            # 'city': city.name,
            'street_list': street_list
        }


@ajax_request
def get_city_adjusters(request):
    adjuster_list = []
    if request.GET.get('city'):
        a_qs = Adjuster.objects.filter(city=int(request.GET.get('city')))
        for i in a_qs:
            adjuster_list.append(
                {
                    'id': i.id,
                    'name': i.user.get_full_name()
                }
            )
        return {
            'success': True,
            'adjuster_list': adjuster_list
        }
    else:
        return {
            'error': True
        }


@ajax_request
def get_area_surface_list(request):
    """
    Функция отображает список поверхностей для постановки задачи.
    Если задача по адресам - показываются только целые и не полностью повреждённые поверхности (флаг damaged=0).
    Если зада на ремонт - показываются только поверхности имеющие повреждения (флаг damaged=1).
    """
    if request.GET.get('area'):
        surface_list = []
        area_pk = int(request.GET.get('area'))
        surface_qs = Surface.objects.filter(street__area=area_pk)
        if request.GET.get('damaged'):
            damaged = int(request.GET.get('damaged'))
            if damaged == 1:
                surface_qs = surface_qs.filter(has_broken=True)
            elif damaged == 0:
                surface_qs = surface_qs.filter(full_broken=False)
        for surface in surface_qs:
            # if surface.id not in client_surfaces:
            if surface.id:
                surface_list.append({
                    'id': surface.id,
                    'city': surface.city.name,
                    'area': surface.street.area.name,
                    'street': surface.street.name,
                    'number': surface.house_number,
                    'porch': surface.porch_count()
                })
        return {
            'surface_list': surface_list
        }
    else:
        return {
            'error': u'Что то пошло не так!'
        }

