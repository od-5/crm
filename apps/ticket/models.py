# coding=utf-8
from django.db import models
from apps.city.models import City
from core.base_model import Common

__author__ = 'alexy'


class Ticket(Common):
    class Meta:
        verbose_name = u'Заявка'
        verbose_name_plural = u'Заявки'
        app_label = 'ticket'

    def __unicode__(self):
        return u'Заявка на имя: %s, телефон: %s' % (self.name, self.phone)

    def performed_at(self):
        pass

    TICKET_TYPE_CHOICE = (
        (0, u'Новая заявка'),
        (1, u'В обработке'),
        (2, u'Отклонена'),
    )

    city = models.ForeignKey(to=City, verbose_name=u'Город', blank=True, null=True)
    name = models.CharField(
        verbose_name=u'Имя',
        max_length=256)
    phone = models.CharField(
        verbose_name=u'Телефон',
        max_length=20,
        blank=True,
        null=True
    )
    text = models.TextField(
        verbose_name=u'Сообщение клиента',
        blank=True,
        null=True)
    type = models.PositiveSmallIntegerField(
        verbose_name=u'Статус заявки',
        choices=TICKET_TYPE_CHOICE,
        default=1,
        blank=True,
        null=True)
    comment = models.TextField(
        verbose_name=u'Комментарий',
        blank=True,
        null=True)
