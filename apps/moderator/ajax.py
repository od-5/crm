# coding=utf-8
from annoying.decorators import ajax_request
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from apps.moderator.forms import ModeratorInfoForm
from apps.moderator.models import ModeratorInfo
from core.models import User

__author__ = 'alexy'


@ajax_request
def moderator_remove(request):
    if request.method == 'GET':
        if request.GET.get('item_id'):
            user = User.objects.get(id=int(request.GET.get('item_id')))
            user.delete()
            return {
                'success': int(request.GET.get('item_id'))
            }
        else:
            return {
                'error': True
            }
    else:
        return {
            'error': True
        }


def moderatorinfo_update(request):
    r_moderator = request.POST.get('moderator')
    user = User.objects.get(id=int(r_moderator))
    moderatorinfo = ModeratorInfo.objects.get(moderator=user)
    if request.method == 'POST':
        form = ModeratorInfoForm(request.POST, instance=moderatorinfo)
        if form.is_valid():
            form.save()
            print 'ok'
    return HttpResponseRedirect(reverse('moderator:change', args=(user.id,)))