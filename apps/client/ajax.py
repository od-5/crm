# coding=utf-8
from annoying.decorators import ajax_request
from datetime import datetime
from apps.adjuster.models import AdjusterTaskSurface
from .models import Client, ClientOrder, ClientJournal, ClientJournalPayment

__author__ = 'alexy'


@ajax_request
def get_client_order_list(request):
    if request.method == 'GET':
        if request.GET.get('client'):
            client = Client.objects.get(id=int(request.GET.get('client')))
            order_list = []
            for order in client.clientorder_set.all():
                order_list.append({
                    'id': order.id,
                    'name': order.__unicode__()
                })
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

            # все адреса (точки) назначения заказа
            order_destinations = order.clientordersurface_set.all()
            co_surface_list_id = [i.surface.id for i in order_destinations]

            # список всех незакрытых точек назначения задачи
            # по списку точек назначения из заказа
            at_surfaces = AdjusterTaskSurface.objects.filter(
                surface__id__in=co_surface_list_id,
                is_closed=False
            )
            at_surface_list_id = [i.surface.id for i in at_surfaces]

            surface_list = []
            for dest in order_destinations:
                broken_porch = []
                intact_porch = []

                if dest.surface.id not in at_surface_list_id:
                    for porch in dest.surface.porch_set.all():
                        if porch.is_broken:
                            broken_porch.append(porch.number)
                        else:
                            intact_porch.append(porch.number)

                    surface_list.append({
                        'id': dest.surface.id,
                        'city': dest.surface.city.name,
                        'area': dest.surface.street.area.name,
                        'street': dest.surface.street.name,
                        'number': dest.surface.house_number,
                        'porch': dest.porch_count(),
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


@ajax_request
def payment_add(request):
    try:
        client = Client.objects.get(pk=int(request.POST.get('p_client')))
        print('client: %s' % client)
        clientjournal = ClientJournal.objects.get(pk=int(request.POST.get('p_clientjournal')))
        print('clientjournal: %s' % clientjournal)
        sum = float(request.POST.get('p_sum'))
        print(sum)
        # import pdb; pdb.set_trace()
        payment = ClientJournalPayment(
            client=client,
            clientjournal=clientjournal,
            sum=sum
        )
        payment.save()
        print('try')
        return {
            'success': True
        }
    except:
        print('except')
        return {
            'error': True
        }
