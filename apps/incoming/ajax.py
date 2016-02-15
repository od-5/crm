# coding=utf-8
from annoying.decorators import ajax_request
from .models import IncomingClient

__author__ = 'alexy'


@ajax_request
def reassign_manager(request):
    pass