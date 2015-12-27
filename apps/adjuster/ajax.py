# coding=utf-8
from annoying.decorators import ajax_request
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
                'id': c_surface.id,
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
