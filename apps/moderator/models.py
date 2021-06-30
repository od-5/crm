# coding=utf-8
from django.db import models
from core.models import User

__author__ = 'alexy'


class ModeratorInfo(models.Model):
    class Meta:
        verbose_name = u'Информация о модераторе'
        verbose_name_plural = u'Информация о модераторах'
        app_label = 'moderator'

    def __unicode__(self):
        return u'Заявка на имя: %s, телефон: %s' % (self.name, self.phone)

    def __str__(self):
        return self.__unicode__()

    MODIFICATION_CHOICES = (
        (1, u'Таблички на подъездах'),
    )
    VALIDITY_CHOICES = (
        (1, u'Неорганичен'),
    )
    RESTRICT_CHOICES = (
        (1, u'Отсутствуют'),
    )

    moderator = models.OneToOneField(on_delete=models.CASCADE,
        to=User,
        verbose_name=u'Модератор'
    )
    modification = models.PositiveSmallIntegerField(
        choices=MODIFICATION_CHOICES,
        verbose_name=u'Модификация',
        default=1
    )
    date = models.DateField(
        verbose_name=u'Дата выдачи',
        blank=True,
        null=True
    )
    validity = models.PositiveSmallIntegerField(
        choices=VALIDITY_CHOICES,
        verbose_name=u'Срок действия',
        default=1
    )
    access_restrictions = models.PositiveSmallIntegerField(
        choices=RESTRICT_CHOICES,
        verbose_name=u'Ограничения доступа',
        default=1
    )
    connection_contract = models.CharField(
        verbose_name=u'Договор подключения к ИПК',
        max_length=200,
        blank=True,
        null=True
    )
    service_contract = models.CharField(
        verbose_name=u'Договор по тех. поддержке и обслуживанию ИПК',
        max_length=200,
        blank=True,
        null=True
    )
    contract_territory = models.CharField(
        verbose_name=u'Территория действия договора',
        max_length=200,
        blank=True,
        null=True
    )
