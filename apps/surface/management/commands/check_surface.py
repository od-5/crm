# coding=utf-8
from django.core.management.base import BaseCommand, CommandError
import datetime
from apps.city.models import Surface

__author__ = 'alexy'


class Command(BaseCommand):

    def handle(self, *args, **options):
        qs = Surface.objects.filter(free=False, release_date__lt=datetime.date.today())
        for surface in qs:
            surface.release_date = datetime.date.today() - datetime.timedelta(days=1)
            surface.free = True
            surface.save()
