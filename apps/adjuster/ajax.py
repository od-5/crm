# coding=utf-8
from annoying.decorators import ajax_request
from django.views.decorators.csrf import csrf_exempt
from apps.adjuster.models import Adjuster

__author__ = 'alexy'


@ajax_request
@csrf_exempt
def adjuster_map(request):
    user = request.user
    adjuster_list = []
    if user.type == 1:
        qs = Adjuster.objects.all()
    elif user.type == 2:
        qs = Adjuster.objects.filter(city__moderator=user)
    elif user.type == 5:
        qs = Adjuster.objects.filter(city__moderator=user.manager.moderator)
    else:
        qs = None
    if request.POST.get('email'):
        qs = qs.filter(user__email=request.POST.get('email'))
    if request.POST.get('last_name'):
        qs = qs.filter(user__last_name=request.POST.get('last_name'))
    if request.POST.get('city') and int(request.POST.get('city')) != 0:
        qs = qs.filter(city__id=int(request.POST.get('city')))
    for i in qs:
        if i.coord_x and i.coord_y:
            adjuster_list.append({
                'coord_x': str(i.coord_x),
                'coord_y': str(i.coord_y),
                'name': i.__unicode__()
            })
    return {
        'adjuster_list': adjuster_list
    }
