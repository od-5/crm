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
            for clientordersurface in order.clientordersurface_set.all():
                print u'Поверхность: %s' % clientordersurface.surface
                broken_porch = []
                intact_porch = []
                for porch in clientordersurface.surface.porch_set.all():
                    print porch
                    if porch.is_broken:
                        broken_porch.append(porch.number)
                    else:
                        intact_porch.append(porch.number)
                print u'Поломанные подъезды: %s' % broken_porch
                print u'Целые подъезды: %s' % intact_porch
                surface_list.append({
                    'id': clientordersurface.surface.id,
                    'city': clientordersurface.surface.city.name,
                    'area': clientordersurface.surface.street.area.name,
                    'street': clientordersurface.surface.street.name,
                    'number': clientordersurface.surface.house_number,
                    'porch': int(clientordersurface.porch_count()),
                    'intact_porch': intact_porch,
                    'broken_porch': broken_porch
                })
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

