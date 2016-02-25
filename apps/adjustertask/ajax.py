# coding=utf-8
from annoying.decorators import ajax_request
from django.views.decorators.csrf import csrf_exempt
from apps.adjuster.models import AdjusterTask, Adjuster
from apps.city.models import Surface
from apps.client.models import Client

__author__ = 'alexy'


@ajax_request
def adjuster_task_client(request):
    if request.GET.get('client'):
        surface_list = []
        print int(request.GET.get('client'))
        client = Client.objects.get(pk=int(request.GET.get('client')))
        print client.clientsurface_set.all()
        for c_surface in client.clientsurface_set.all():
            surface_list.append({
                'id': c_surface.surface.id,
                'area': c_surface.surface.street.area.name,
                'street': c_surface.surface.street.name,
                'number': c_surface.surface.house_number,
            })
        return {
            'surface_list': surface_list
        }
    return {
        'error': 'Warning!'
    }


@ajax_request
@csrf_exempt
def adjuster_get_area_streets(request):
    if request.GET.get('area'):
        surface_list = []
        area_pk = int(request.GET.get('area'))

        surface_qs = Surface.objects.filter(street__area=area_pk)
        for surface in surface_qs:
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
def ajax_order_adjuster_list(request):
    r_client = request.GET.get('client')
    print r_client
    if int(r_client) != 0:
        client = Client.objects.get(pk=int(r_client))
        print client
        adjuster_qs = Adjuster.objects.filter(city=client.city)
        print adjuster_qs
        clientorder_qs = client.clientorder_set.all()
        print clientorder_qs
        adjuster_list = []
        clientorder_list = []
        for adjuster in adjuster_qs:
            adjuster_list.append({
                'id': adjuster.id,
                'name': adjuster.user.get_full_name()
            })
        for clientorder in clientorder_qs:
            clientorder_list.append({
                'id': clientorder.id,
                'name': clientorder.__unicode__()
            })
        print adjuster_list
        print clientorder_list
        return {
            'adjuster_list': adjuster_list,
            'clientorder_list': clientorder_list
        }
    else:
        print 'else'
        return {
            'error': u'Что то пошло не так!'
        }
