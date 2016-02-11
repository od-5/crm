# coding=utf-8
from annoying.decorators import ajax_request
from django.shortcuts import get_object_or_404
from apps.city.models import City, Surface, Porch, Area, Street, ManagementCompany
from core.models import User
from apps.client.models import Client, ClientMaket, ClientOrder, ClientOrderSurface, ClientJournal
from apps.adjuster.models import Adjuster, AdjusterTask, AdjusterTaskSurface
from apps.manager.models import Manager


__author__ = 'alexy'


@ajax_request
def ymap(request):
    request.encoding = 'utf-8'
    if request.is_ajax():
        if request.user.type == 1:
            query = City.objects.all()
        else:
            query = City.objects.filter(moderator=request.user)
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
    request.encoding = 'utf-8'
    print 'step 1'
    if request.is_ajax():
        if request.user.type == 1:
            query = Surface.objects.all()
            print 'admin'
        else:
            query = Surface.objects.filter(city__moderator=request.user)
            print 'moderator'
        result = []
        print 'query = %s' % query
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
    print 'data = %s' % data
    return data


@ajax_request
def ajax_remove_item(request):
    if request.method == 'GET':
        print 'request = GET'
        if request.GET.get('item_id') and request.GET.get('item_model'):
            model = request.GET.get('item_model')
            item_id = request.GET.get('item_id')
            print model
            print item_id
            # client = Client.objects.get(id=int(request.GET.get('item_id')))
            # user = User.objects.get(pk=client.user.id)
            item = get_object_or_404(eval(model), pk=int(item_id))
            print item
            if model == 'Client':
                print 'delete client user'
                user = User.objects.get(pk=item.user.id)
                user.delete()
            if model == 'Manager':
                print 'delete manager user'
                user = User.objects.get(pk=item.user.id)
                user.delete()
            if model == 'Adjuster':
                print 'delete adjuster user'
                user = User.objects.get(pk=item.user.id)
                user.delete()
            if model == 'ClientOrderSurface':
                surface = Surface.objects.get(pk=item.surface.id)
                surface.free = True
                surface.save()
            item.delete()
            return {
                'id': int(request.GET.get('item_id')),
                'model': request.GET.get('item_model'),
            }
        else:
            print 'not element in request'
            return {
                'error': True
            }
    else:
        print 'request != GET'
        return {
            'error': True
        }
