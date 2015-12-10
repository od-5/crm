# coding=utf-8
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
import core.geotagging as api
from core.models import User

__author__ = 'alexy'


api_key = settings.YANDEX_MAPS_API_KEY


class City(models.Model):
    class Meta:
        verbose_name = u'Город'
        verbose_name_plural = u'Города'
        app_label = 'city'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('city:change', args=(self.pk, ))

    def save(self, *args, **kwargs):
        pos = api.geocode(api_key, self)
        self.coord_x = float(pos[0])
        self.coord_y = float(pos[1])
        super(City, self).save()

    name = models.CharField(max_length=100, verbose_name=u'Город')
    moderator = models.ForeignKey(to=User, blank=True, null=True, verbose_name=u'Модератор')
    contract_number = models.CharField(max_length=100, blank=True, null=True, verbose_name=u'Номер договора')
    contract_date = models.DateField(blank=True, null=True, verbose_name=u'Договор от')
    coord_x = models.DecimalField(max_digits=8, decimal_places=6, blank=True, null=True, verbose_name=u'Ширина')
    coord_y = models.DecimalField(max_digits=8, decimal_places=6, blank=True, null=True, verbose_name=u'Долгота')


class Area(models.Model):
    class Meta:
        verbose_name = u'Район'
        verbose_name_plural = u'Районы'
        app_label = 'city'

    def __unicode__(self):
        return self.name

    city = models.ForeignKey(to=City, verbose_name=u'Город')
    name = models.CharField(max_length=100, verbose_name=u'Название')


class ConstructionType(models.Model):
    class Meta:
        verbose_name = u'Вид конструкции'
        verbose_name_plural = u'Виды конструкций'
        app_label = 'city'

    def __unicode__(self):
        return self.format

    city = models.ForeignKey(to=City, verbose_name=u'Город')
    format = models.CharField(max_length=100, verbose_name=u'Формат')
    price = models.PositiveIntegerField(verbose_name=u'Цена')


class Surface(models.Model):
    class Meta:
        verbose_name = u'Поверхность'
        verbose_name_plural = u'Поверхности'
        app_label = 'city'

    def __unicode__(self):
        return u'Город %s, район %s, %s, %s' % (self.city, self.area, self.street, self.house_number)

    def get_absolute_url(self):
        return reverse('city:surface-change', args=(self.pk, ))

    city = models.ForeignKey(to=City, verbose_name=u'Город')
    area = models.ForeignKey(to=Area, verbose_name=u'Район')
    street = models.CharField(max_length=256, verbose_name=u'Улица')
    house_number = models.CharField(max_length=50, verbose_name=u'Номер дома')


class Porch(models.Model):
    class Meta:
        verbose_name = u'Подъезд'
        verbose_name_plural = u'Подъезды'
        app_label = 'city'

    def __unicode__(self):
        return u'Подъезд № %s' % self.number

    surface = models.ForeignKey(to=Surface, verbose_name=u'Рекламная поверхность')
    number = models.CharField(max_length=10, verbose_name=u'Номер подъезда')