# coding=utf-8
from annoying.decorators import ajax_request
from datetime import datetime
from .models import IncomingClient, IncomingTask, IncomingClientContact
from apps.manager.models import Manager
from .models import IncomingClient, IncomingClientManager

__author__ = 'alexy'


@ajax_request
def reassign_manager(request):
    old_id = int(request.GET.get('manager'))
    new_id = int(request.GET.get('new_manager'))
    new_manager = Manager.objects.get(pk=new_id)
    incomingclient_id = int(request.GET.get('incomingclient'))
    incomingclient = IncomingClient.objects.get(pk=incomingclient_id)
    tasks = IncomingTask.objects.filter(incomingclient=incomingclient_id)
    if tasks.count() != 0:
        for task in tasks:
            task.manager = new_manager
            task.save()

    incomingclient.manager = new_manager
    incomingclient.save()
    new_incomingclientmanager = IncomingClientManager(manager=new_manager, incomingclient=incomingclient)
    new_incomingclientmanager.save()
    return {
        'success': True,
        'old_id': old_id,
        'incomingclient_id': incomingclient.id,
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


@ajax_request
def get_contact_list(request):
    contact_list = []
    incomingclient = IncomingClient.objects.get(pk=int(request.GET.get('incomingclient')))
    for contact in incomingclient.incomingclientcontact_set.all():
        contact_list.append({
            'name': contact.name,
            'function': contact.function,
            'phone': contact.phone,
            'email': contact.email,
        })
    if len(contact_list) != 0:
        return {
            'contact_list': contact_list
        }
    else:
        return {
            'nothing': True
        }


@ajax_request
def get_incomingclient_info(request):
    incomingclient = IncomingClient.objects.get(pk=int(request.GET.get('incomingclient')))
    contact_list = []
    for i in incomingclient.incomingclientcontact_set.all():
        contact_list.append({
            'id': i.id,
            'name': i.name
        })
    return {
        'id': incomingclient.id,
        'name': incomingclient.name,
        'type': incomingclient.get_type_display(),
        'contact_list': contact_list
    }


@ajax_request
def ajax_task_add(request):
    incomingclient = IncomingClient.objects.get(pk=int(request.GET.get('incomingclient')))
    type = int(request.GET.get('type'))
    date = datetime.strptime(request.GET.get('date'), '%d.%m.%Y')
    comment = request.GET.get('comment')
    manager = Manager.objects.get(pk=int(request.GET.get('manager')))
    incomingclient_contact = IncomingClientContact.objects.get(pk=int(request.GET.get('incomingclient_contact')))
    try:
        task = IncomingTask(
            manager=manager,
            incomingclient=incomingclient,
            incomingclientcontact=incomingclient_contact,
            type=type,
            date=date,
            comment=comment,
            status=0
        )
        task.save()
        return {
            'success': True
        }
    except:
        return {
            'success': False
        }
