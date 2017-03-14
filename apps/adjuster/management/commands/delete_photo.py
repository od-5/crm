# coding=utf-8
import os
import datetime

from django.core.management.base import BaseCommand, CommandError

from apps.adjuster.models import SurfacePhoto

__author__ = 'alexy'


class Command(BaseCommand):

    def handle(self, *args, **options):
        search_date = datetime.datetime.now() - datetime.timedelta(days=182)
        qs = SurfacePhoto.objects.filter(date__lt=search_date)
        print qs.count()
        if qs:
            qs.delete()
