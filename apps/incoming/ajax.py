# coding=utf-8
from annoying.decorators import ajax_request
from .models import IncomingClient, IncomingTask
from apps.manager.models import Manager

__author__ = 'alexy'


@ajax_request
def reassign_manager(request):
    old_id = int(request.GET.get('manager'))
    new_id = int(request.GET.get('new_manager'))
    new_manager = Manager.objects.get(pk=new_id)
    incomingclient_id = int(request.GET.get('incomingclient'))
    incomingclient = IncomingClient.objects.get(pk=incomingclient_id)
    tasks = IncomingTask.objects.filter(incomingclient=incomingclient_id)
    if tasks.count() != 0 :
        for task in tasks:
            task.manager = new_manager
            task.save()

    incomingclient.manager = new_manager
    incomingclient.save()
    return {
        'success': True,
        'old_id': old_id,
        'id': new_id,
        'name': incomingclient.manager.user.get_full_name(),
    }

@ajax_request
def get_available_manager_list(request):
    manager_list = []
    current_manager = Manager.objects.get(pk=int(request.GET.get('manager')))
    manager_qs = Manager.objects.filter(moderator=current_manager.moderator.id)
    for manager in manager_qs:
        manager_list.append({
            'id': manager.id,
            'name': manager.user.get_full_name()
        })
    return {
        'manager_list': manager_list
    }