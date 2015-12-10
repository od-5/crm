# coding=utf-8
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from apps.city.models import City
from core.models import User

__author__ = 'alexy'


class Client(models.Model):
    class Meta:
        verbose_name = u'Клиент'
        verbose_name_plural = u'Клиенты'
        app_label = 'client'

    def __unicode__(self):
        return self.legal_name

    user = models.OneToOneField(to=User, verbose_name=u'Пользователь')
    city = models.ForeignKey(to=City, verbose_name=u'Город')
    legal_name = models.CharField(max_length=256, blank=True, null=True, verbose_name=u'Юридическое название')
    actual_name = models.CharField(max_length=256, blank=True, null=True, verbose_name=u'Фактичексое название')
    inn = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'ИНН')
    kpp = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'КПП')
    legal_address = models.TextField(verbose_name=u'Физический адрес', blank=True, null=True)
    leader = models.CharField(max_length=100, blank=True, null=True, verbose_name=u'Руководитель')
    leader_function = models.CharField(max_length=100, blank=True, null=True, verbose_name=u'Должноть руководителя')
    work_basis = models.CharField(max_length=256, blank=True, null=True, verbose_name=u'Основание для работы')
