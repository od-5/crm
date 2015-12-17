# coding=utf-8
from annoying.decorators import ajax_request
from apps.city.models import City, Surface

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
            result_json['coord_x'] = float(item.coord_x)
            result_json['coord_y'] = float(item.coord_y)
            result.append(result_json)
        data = result

    else:
        data = {'msg': 'fail'}
    print 'data = %s' % data
    return data
