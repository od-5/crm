# coding = utf-8
__author__ = 'alexy'
import datetime
from apps.city.models import Surface

# todo: сделать команду и поставить в cron на хостинге, ежедневно в 12 ночи проверять release_date
qs = Surface.objects.filter(free=False, release_date__lte=datetime.date.today())

for surface in qs:
    surface.release_date = datetime.date.today() - datetime.timedelta(days=1)
    surface.free = True
    surface.save()
