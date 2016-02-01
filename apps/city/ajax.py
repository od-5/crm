# coding=utf-8
from annoying.decorators import ajax_request
from apps.adjuster.models import Adjuster
from apps.city.forms import AreaAddForm, StreetForm
from apps.city.models import Area, City, Street, Surface, Porch
from apps.client.models import Client, ClientSurface
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
def get_area_streets(request):
    if request.GET.get('area') and request.GET.get('client'):
        surface_list = []
        area_pk = int(request.GET.get('area'))

        surface_qs = Surface.objects.filter(street__area=area_pk, free=True)
        # TODO: сделать проверку поверхностей. Выводить только те, которые ещё никто не заказал, и которые будут свободны на начало указанной даты заказа
        # try:
        #     client = Client.objects.get(id=int(request.GET.get('client')))
        #     # print(surface_qs & ClientSurface.objects.filter(client=client))
        #     client_surfaces = []
        #     for item in ClientSurface.objects.filter(client=client):
        #         client_surfaces.append(item.surface.id)
        #         #     surface_qs = surface_qs.exclude(surface=item.surface)
        # except:
        #     pass
        for surface in surface_qs:
            # if surface.id not in client_surfaces:
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
    if request.GET.get('area'):
        surface_list = []
        area_pk = int(request.GET.get('area'))
        # TODO: продумать queryset - только свободные поверхности показывать или только занятые?
        surface_qs = Surface.objects.filter(street__area=area_pk)
        if request.GET.get('damaged'):
            damaged = int(request.GET.get('damaged'))
            if damaged == 1:
                surface_qs = surface_qs.filter(has_broken=True)
            else:
                surface_qs = surface_qs.filter(has_broken=False)
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

