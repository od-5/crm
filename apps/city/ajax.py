# coding=utf-8
from annoying.decorators import ajax_request
from apps.city.models import Area, City, Street
from core.models import User

__author__ = 'alexy'

# @ajax_request
# def surface_list_filter(request):
#     user = request.user
#     print user
#     print type(user)
#     if request.POST.get('city_filter'):
#         qs = Area.objects.filter(city__id=int(request.POST.get('city_filter')))


@ajax_request
def surface_ajax(request):
    street_list = []
    if request.GET.get('city'):
        print request.GET.get('city')
        if int(request.GET.get('city')) == 0:
            print 'Null'
            user = User.objects.get(id=int(request.user.id))
            print user
            if user.type == 1:
                city = City.objects.all()
                street_qs = Street.objects.all()
                print 'admin'
            else:
                city = user.city_set.all()
                street_qs = Street.objects.filter(city__moderator=user)
                print city
                print 'not admin'
        else:
            print 'Not null'
            city = City.objects.get(id=int(request.GET.get('city')))
            street_qs = city.street_set.all()
        print city
        print street_qs
        for i in street_qs:
            street_list.append(
                {
                    'id': i.id,
                    'name': i.name
                }
            )
        return {
            # 'city': city.name,
            'street_list': street_list
        }
