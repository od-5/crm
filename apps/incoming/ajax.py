# coding=utf-8
from annoying.decorators import ajax_request
from datetime import datetime
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, JsonResponse
from apps.client.models import Client
from core.models import User
from .models import IncomingClient, IncomingTask, IncomingClientContact
from apps.manager.models import Manager
from .models import IncomingClient, IncomingClientManager

__author__ = 'alexy'


@ajax_request
def reassign_manager(request):
    old_id = int(request.GET.get('manager'))
    new_id = int(request.GET.get('new_manager'))

    incomingclient_id = int(request.GET.get('incomingclient'))
    if old_id != new_id:
        incomingclient = IncomingClient.objects.get(pk=incomingclient_id)
        new_manager = Manager.objects.get(pk=new_id)
        incomingclient.manager = new_manager
        incomingclient.type = 2
        incomingclient.save()
        new_incomingclientmanager = IncomingClientManager(manager=new_manager, incomingclient=incomingclient)
        new_incomingclientmanager.save()
        tasks = IncomingTask.objects.filter(incomingclient=incomingclient_id)
        if tasks.count() != 0:
            for task in tasks:
                task.manager = new_manager
                task.save()
        return {
            'success': True,
            'old_id': old_id,
            'incomingclient_id': incomingclient.id,
            'id': new_id,
            'name': incomingclient.manager.user.get_full_name(),
        }
    else:
        return {
            'success': False,
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
            'id': contact.id,
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
        'manager': incomingclient.manager.id,
        'type': incomingclient.get_type_display(),
        'contact_list': contact_list
    }


@ajax_request
def get_incomingtask_info(request):
    incomingtask = IncomingTask.objects.get(pk=int(request.GET.get('incomingtask')))
    contact_list = []
    for i in incomingtask.incomingclient.incomingclientcontact_set.all():
        contact_list.append({
            'id': i.id,
            'name': i.name
        })
    return {
        'incomingtask_id': incomingtask.id,
        'incomingclient_id': incomingtask.incomingclient.id,
        'incomingclient_name': incomingtask.incomingclient.name,
        'manager_id': incomingtask.manager.id,
        'incomingclient_type': incomingtask.incomingclient.get_type_display(),
        'contact_list': contact_list
    }


@ajax_request
def ajax_task_add(request):
    try:
        incomingclient = IncomingClient.objects.get(pk=int(request.GET.get('incomingclient')))
        type_id = int(request.GET.get('type'))
        date = datetime.strptime(request.GET.get('date'), '%d.%m.%Y')
        comment = request.GET.get('comment')
        manager = Manager.objects.get(pk=int(request.GET.get('manager')))
        incomingclientcontact = IncomingClientContact.objects.get(pk=int(request.GET.get('incomingclient_contact')))
        task = IncomingTask(
            manager=manager,
            incomingclient=incomingclient,
            incomingclientcontact=incomingclientcontact,
            type=type_id,
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


@ajax_request
def ajax_task_update(request):
    try:
        manager_id = int(request.GET.get('manager'))
        incomingclient_id = int(request.GET.get('incomingclient'))
        incomingtask_id = int(request.GET.get('incomingtask'))
        incomingclient_contact_id = int(request.GET.get('incomingclient_contact'))
        type_id = int(request.GET.get('type'))
        comment = request.GET.get('comment')
        date = datetime.strptime(request.GET.get('date'), '%d.%m.%Y')

        incomingclient = IncomingClient.objects.get(pk=incomingclient_id)
        incomingtask = IncomingTask.objects.get(pk=incomingtask_id)
        manager = Manager.objects.get(pk=manager_id)
        incomingclientcontact = IncomingClientContact.objects.get(pk=incomingclient_contact_id)
        task = IncomingTask(
            manager=manager,
            incomingclient=incomingclient,
            incomingclientcontact=incomingclientcontact,
            type=type_id,
            date=date,
            comment=comment,
            status=0
        )
        task.save()
        incomingtask.status = 1
        incomingtask.save()
        return {
            'success': True
        }
    except:
        return {
            'success': False
        }


def ajax_client_add(request):
    r_incomingclient = request.POST.get('incomingclient')
    r_manager = request.POST.get('manager')
    r_incomingtask = request.POST.get('incomingtask')
    r_incomingcontact = request.POST.get('incomingcontact')
    r_date = request.POST.get('date')
    r_comment = request.POST.get('comment')
    r_email = request.POST.get('email')
    r_password = request.POST.get('password')
    incomingclient = IncomingClient.objects.get(pk=int(r_incomingclient))
    incomingtask = IncomingTask.objects.get(pk=int(r_incomingtask))
    if r_incomingcontact:
        incomingcontact = IncomingClientContact.objects.get(pk=int(r_incomingcontact))
    else:
        incomingcontact = incomingtask.incomingclientcontact
    manager = Manager.objects.get(pk=int(r_manager))
    try:
        User.objects.get(email=r_email)
    except User.DoesNotExist:
        user = User(email=r_email, password=r_password, type=3)
        user.set_password(r_password)
        user.save()
        client = Client(
            user=user,
            city=incomingclient.city,
            manager=incomingclient.manager,
            legal_name=incomingclient.name,
            actual_name=incomingclient.name,
            legal_address=incomingclient.actual_address
        )
        client.save()
        incomingtask.status = 1
        incomingtask.save()
        return HttpResponseRedirect(reverse('client:change', args=(client.id, )))
    return_url = reverse('incoming:task-list') + '?error=1'
    return HttpResponseRedirect(return_url)
