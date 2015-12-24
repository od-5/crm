# coding=utf-8
from annoying.decorators import ajax_request
from apps.city.models import Area, City, Street, Surface, Porch
from apps.client.models import Client, ClientSurface
from core.models import User

__author__ = 'alexy'


@ajax_request
def task_add_filter(request):
    if request.GET.get('surface'):
        porch_list = []
        if int(request.GET.get('surface')) != 0:
            porch_qs = Porch.objects.filter(surface=int(request.GET.get('surface')))
            for porch in porch_qs:
                porch_list.append({
                    'id': porch.id,
                    'number': porch.number
                })
            print porch_list
            return {
                'porch_list': porch_list
            }
        else:
            return {
                'error': 'ACHTUNG!!!'
            }
