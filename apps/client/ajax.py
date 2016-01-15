# coding=utf-8
from annoying.decorators import ajax_request
from .models import Client, ClientOrder

__author__ = 'alexy'


@ajax_request
def get_client_order_list(request):
    if request.method == 'GET':
        if request.GET.get('client'):
            client = Client.objects.get(id=int(request.GET.get('client')))
            print Client
            order_list = []
            for order in client.clientorder_set.all():
                print order
                order_list.append({
                    'id': order.id,
                    'name': order.__unicode__()
                })
            print order_list
            return {
                'success': True,
                'order_list': order_list
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
def get_client_order_address_list(request):
    if request.method == 'GET':
        if request.GET.get('clientorder'):
            order = ClientOrder.objects.get(id=int(request.GET.get('clientorder')))
            print order
            surface_list = []
            for surface in order.clientordersurface_set.all():
                surface_list.append({
                    'id': surface.id,
                    'city': surface.surface.city.name,
                    'area': surface.surface.street.area.name,
                    'street': surface.surface.street.name,
                    'number': surface.surface.house_number,
                    'porch': int(surface.porch_count())
                })
            print surface_list
            return {
                'success': True,
                'surface_list': surface_list
            }
        else:
            return {
                'error': True
            }
    else:
        return {
            'error': True
        }

