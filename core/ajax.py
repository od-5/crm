# coding=utf-8
import datetime
from django.utils.timezone import utc
from annoying.decorators import ajax_request
from django.shortcuts import get_object_or_404
from apps.city.models import City, Surface, Porch, Area, Street, ManagementCompany
from core.models import User
from apps.client.models import Client, ClientMaket, ClientOrder, ClientOrderSurface, ClientJournal, ClientJournalPayment
from apps.adjuster.models import Adjuster, AdjusterTask, AdjusterTaskSurface
from apps.manager.models import Manager
from apps.incoming.models import IncomingClient, IncomingTask, IncomingClientContact
from apps.landing.models import Setup, BlockEffective, BlockReview, BlockExample
from apps.ticket.models import Ticket


__author__ = 'alexy'


@ajax_request
def ymap(request):
    request.encoding = 'utf-8'
    if request.is_ajax():
        query = City.objects.all()
        try:
            if request.user.type == 2:
                query = query.filter(moderator=request.user)
        except:
            pass
        result = []
        for item in query:
            result_json = {}
            result_json['name'] = u'%s (%s)' % (item.name, item.surface_count())
            result_json['coord_x'] = float(item.coord_x)
            result_json['coord_y'] = float(item.coord_y)
            result.append(result_json)
        data = result
    else:
        data = {'msg': 'fail'}
    return data


@ajax_request
def ymap_surface(request):
    user = request.user
    request.encoding = 'utf-8'
    if request.is_ajax():
        if user.type == 1:
            query = Surface.objects.all()
        elif user.type == 6:
            query = Surface.objects.filter(city__in=user.superviser.city_id_list())
        elif user.type == 2:
            query = Surface.objects.filter(city__moderator=user)
        elif user.type == 5:
            query = Surface.objects.filter(city__moderator=user.manager.moderator)
        else:
            query = None
        result = []
        for item in query:
            result_json = {}
            result_json['name'] = u'%s %s' % (item.street.name, item.house_number)
            result_json['porch'] = item.porch_set.count()
            result_json['coord_x'] = float(item.coord_x)
            result_json['coord_y'] = float(item.coord_y)
            result.append(result_json)
        data = result

    else:
        data = {'msg': 'fail'}
    return data


@ajax_request
def ajax_remove_item(request):
    if request.method == 'GET':
        if request.GET.get('item_id') and request.GET.get('item_model'):
            model = request.GET.get('item_model')
            item_id = request.GET.get('item_id')
            item = get_object_or_404(eval(model), pk=int(item_id))
            if model == 'Client':
                for order in item.clientorder_set.all():
                    order.delete()
                for journal in item.clientjournal_set.all():
                    journal.delete()
                for pay in item.clientjournalpayment_set.all():
                    pay.delete()
                user = User.objects.get(pk=item.user.id)
                user.delete()
            if model == 'Manager':
                user = User.objects.get(pk=item.user.id)
                user.delete()
            if model == 'Adjuster':
                for at in item.adjustertask_set.all():
                    for ats in at.adjustertasksurface_set.all():
                        for atsp in ats.adjustertasksurfaceporch_set.all():
                            atsp.delete()
                        ats.delete()
                    at.delete()
                user = User.objects.get(pk=item.user.id)
                user.delete()
            if model == 'AdjusterTask':
                for ats in item.adjustertasksurface_set.select_related().all():
                    for atsp in ats.adjustertasksurfaceporch_set.all():
                        atsp.delete()
                    ats.delete()
            if model == 'AdjusterTaskSurface':
                for atsp in item.adjustertasksurfaceporch_set.all():
                    atsp.delete()
            if model == 'ClientOrderSurface':
                release_date = datetime.datetime.utcnow().replace(tzinfo=utc) - datetime.timedelta(days=1)
                surface = Surface.objects.get(pk=item.surface.id)
                surface.free = True
                surface.release_date = release_date.date()
                surface.save()
            item.delete()
            return {
                'id': int(request.GET.get('item_id')),
                'model': request.GET.get('item_model'),
            }
        else:
            return {
                'error': True
            }
    else:
        return {
            'error': True
        }
