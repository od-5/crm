# coding=utf-8
from django.core.management.base import BaseCommand, CommandError
import datetime
from apps.client.models import ClientOrder

__author__ = 'alexy'


class Command(BaseCommand):

    def handle(self, *args, **options):
        qs = ClientOrder.objects.filter(is_closed=False, date_end__lt=datetime.date.today())
        for order in qs:
            order.is_closed = True
            order.save()
