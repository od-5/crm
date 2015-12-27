# coding=utf-8
from annoying.decorators import ajax_request
from core.models import User

__author__ = 'alexy'


@ajax_request
def administrator_remove(request):
    if request.method == 'GET':
        if request.GET.get('item_id'):
            user = User.objects.get(id=int(request.GET.get('item_id')))
            print user
            user.delete()
            return {
                'success': int(request.GET.get('item_id'))
            }
        else:
            print 'no element'
            return {
                'error': True
            }
    else:
        print 'error'
        return {
            'error': True
        }
