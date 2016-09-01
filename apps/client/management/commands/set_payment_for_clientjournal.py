# coding=utf-8
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Sum
from apps.client.models import ClientJournal

__author__ = 'alexy'


class Command(BaseCommand):

    def handle(self, *args, **options):
        qs = ClientJournal.objects.all()
        for item in qs:
            item.total_payment = item.clientjournalpayment_set.all().aggregate(Sum('sum'))['sum__sum']
            item.save()