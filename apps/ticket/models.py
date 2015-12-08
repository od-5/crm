# coding=utf-8
from django.db import models
from core.base_model import Common

__author__ = 'alexy'


class Ticket(Common):
    class Meta:
        verbose_name = u'Заявка'
        verbose_name_plural = u'Заявки'
        app_label = 'ticket'

    def __unicode__(self):
        return self.name

    def performed_at(self):
        pass

    TICKET_STATUS_CHOICE = (
        (0, u'В обработке'),
        (1, u'Новая заявка'),
        (2, u'Отклонена'),
        (3, u'Нет ответа'),
    )

    SALE_STATUS_CHOICE = (
        (0, u'Ожидание оплаты'),
        (1, u'Уточнение деталей'),
        (2, u'Оплачено'),
        (3, u'Выполнено'),
    )

    name = models.CharField(verbose_name=u'Имя', max_length=256)
    email = models.EmailField(verbose_name=u'e-mail', max_length=256)
    comment = models.TextField(verbose_name=u'Сообщение клиента', blank=True, null=True)
    sale = models.BooleanField(verbose_name=u'Продажа', default=False)
    ticket_status = models.PositiveSmallIntegerField(verbose_name=u'Статус заявки',  choices=TICKET_STATUS_CHOICE, default=1, blank=True, null=True)
    ticket_comment = models.TextField(verbose_name=u'Комментарий', blank=True, null=True)
    sale_status = models.PositiveSmallIntegerField(verbose_name=u'Статус продажи', choices=SALE_STATUS_CHOICE, default=1, blank=True, null=True)
    sale_comment = models.TextField(verbose_name=u'Комментарий', blank=True, null=True)
    price = models.PositiveIntegerField(verbose_name=u'Сумма', default=0, blank=True, null=True)
