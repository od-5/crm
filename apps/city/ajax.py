# coding=utf-8
from annoying.decorators import ajax_request
from apps.city.forms import AreaAddForm, StreetForm
from apps.city.models import Area, City, Street, Surface, Porch
from apps.client.models import Client, ClientSurface
from apps.surface.forms import PorchAddForm
from core.models import User

__author__ = 'alexy'


@ajax_request
def get_city_area(request):
    if request.GET.get('city_id'):
        area_list = []
        area_qs = City.objects.get(pk=int(request.GET.get('city_id'))).area_set.all()
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
