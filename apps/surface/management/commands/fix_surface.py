# coding=utf-8
from django.core.management.base import BaseCommand, CommandError
import datetime
from apps.city.models import Surface

__author__ = 'alexy'


class Command(BaseCommand):

    def handle(self, *args, **options):
        qs = Surface.objects.filter(free=False)
        for surface in qs:
            if surface.clientordersurface_set.count() == 0:
                surface.release_date = datetime.date.today() - datetime.timedelta(days=10)
                surface.free = True
                surface.save()
