# coding=utf-8
from django.core.management.base import BaseCommand, CommandError
from apps.city.models import Surface

__author__ = 'alexy'


class Command(BaseCommand):

    def handle(self, *args, **options):
        qs = Surface.objects.all()
        for surface in qs:
            surface.porch_total_count = surface.porch_count()
            surface.save()
