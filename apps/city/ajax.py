# coding=utf-8
from annoying.decorators import ajax_request
from apps.city.forms import AreaAddForm, StreetForm
from apps.city.models import Area, City, Street, Surface
from apps.client.models import Client, ClientSurface
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

        surface_qs = Surface.objects.filter(street__area=area_pk)
        try:
            client = Client.objects.get(id=int(request.GET.get('client')))
            # print(surface_qs & ClientSurface.objects.filter(client=client))
            client_surfaces = []
            for item in ClientSurface.objects.filter(client=client):
                client_surfaces.append(item.surface.id)
                #     surface_qs = surface_qs.exclude(surface=item.surface)
        except:
            pass
        for surface in surface_qs:
            if surface.id not in client_surfaces:
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
def city_remove(request):
    if request.method == 'GET':
        if request.GET.get('item_id'):
            city = City.objects.get(id=int(request.GET.get('item_id')))
            city.delete()
            return {
                'success': int(request.GET.get('item_id'))
            }
        else:
            return {
                'error': True
            }
    else:
        return {
            'error': True
        }


@ajax_request
def area_add(request):
    if request.method == 'POST':
        form = AreaAddForm(request.POST)
        if form.is_valid():
            instance = form.save()
            return {
                'success': True,
                'id': instance.id,
                'name': instance.name
            }
        else:
            return {
                'error': u'Ошибка'
            }
    else:
        return {
            'error': u'Ошибка'
        }


@ajax_request
def area_remove(request):
    if request.method == 'GET':
        if request.GET.get('item_id'):
            area = Area.objects.get(id=int(request.GET.get('item_id')))
            area.delete()
            return {
                'success': int(request.GET.get('item_id'))
            }
        else:
            return {
                'error': True
            }
    else:
        return {
            'error': True
        }


@ajax_request
def area_update(request):
    r_id = request.GET.get('item_id')
    r_name = request.GET.get('item_name')
    area = Area.objects.get(pk=int(r_id))
    if r_name and r_name.strip() != '':
        area.name = r_name
        area.save()
        return {
            'success': True,
            'id': area.id,
            'name': area.name
        }
    else:
        return {
            'error': True
        }


@ajax_request
def street_add(request):
    if request.method == 'POST':
        form = StreetForm(request.POST)
        if form.is_valid():
            instance = form.save()
            return {
                'success': True,
                'id': instance.id,
                'area': instance.area.name,
                'name': instance.name
            }
        else:
            return {
                'error': True
            }
    else:
        return {
            'error': True
        }


@ajax_request
def street_remove(request):
    if request.method == 'GET':
        if request.GET.get('item_id'):
            street = Street.objects.get(id=int(request.GET.get('item_id')))
            street.delete()
            return {
                'success': int(request.GET.get('item_id'))
            }
        else:
            return {
                'error': True
            }
    else:
        return {
            'error': True
        }


@ajax_request
def street_update(request):
    r_id = request.GET.get('item_id')
    r_name = request.GET.get('item_name')
    street = Street.objects.get(pk=int(r_id))
    if r_name and r_name.strip() != '':
        street.name = r_name
        street.save()
        return {
            'success': True,
            'id': street.id,
            'name': street.name
        }
    else:
        return {
            'error': True
        }
