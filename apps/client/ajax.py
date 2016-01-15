# coding=utf-8
from annoying.decorators import ajax_request
from django.shortcuts import get_object_or_404
from .models import Client
from core.models import User

__author__ = 'alexy'


@ajax_request
def client_remove(request):
    if request.method == 'GET':
        if request.GET.get('item_id'):
            client = Client.objects.get(id=int(request.GET.get('item_id')))
            user = User.objects.get(pk=client.user.id)
            client.delete()
            user.delete()
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
