# coding=utf-8
from datetime import datetime
from annoying.decorators import ajax_request
from django.views.decorators.csrf import csrf_exempt
from apps.city.models import Surface

__author__ = 'alexy'


@ajax_request
@csrf_exempt
def surface_map(request):
    user = request.user
    surface_list = []
    if user.type == 1:
        qs = Surface.objects.select_related().all()
    elif user.type == 6:
            qs = Surface.objects.select_related().filter(city__in=user.superviser.city_id_list())
    elif user.type == 2:
        qs = Surface.objects.select_related().filter(city__moderator=user)
    elif user.type == 5:
        qs = Surface.objects.select_related().filter(city__moderator=user.manager.moderator)
    else:
        qs = None
    # фильтрация поверхностей по городам, районам, улицам
    management = request.POST.get('management')
    city = request.POST.get('city')
    area = request.POST.get('area')
    street = request.POST.get('street')
    release_date = request.POST.get('release_date')
    free = request.POST.get('free')
    if management:
        if int(management) == 0:
            qs = qs
        elif int(management) == -1:
            qs = qs.filter(management__isnull=True)
        else:
            qs = qs.filter(management=int(management))
    if city and int(city) != 0:
        qs = qs.filter(city=int(city))
    if area and int(area) != 0:
        qs = qs.filter(street__area=int(area))
    if street and int(street) != 0:
        qs = qs.filter(street=int(street))
    if release_date:
        qs = qs.filter(release_date__lte=datetime.strptime(release_date, '%d.%m.%Y'))
    if free:
        if int(free) == 1:
            qs = qs.filter(free=True)
        if int(free) == 2:
            qs = qs.filter(free=False)
    for surface in qs:
        surface_list.append({
            'coord_y': surface.coord_y,
            'coord_x': surface.coord_x,
            'name': surface.__unicode__(),
            'porch_count': surface.porch_total_count
        })
    return {
        'surface_list': surface_list
    }
