# coding=utf-8
from annoying.functions import get_object_or_None
from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.city.models import City
from apps.landing.models import Setup
from core.base_model import Common

__author__ = 'alexy'


class Ticket(Common):
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
    email = models.CharField(
        verbose_name=u'Email',
        max_length=30,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = u'Заявка'
        verbose_name_plural = u'Заявки'
        app_label = 'ticket'
        ordering = ['-created', ]

    def __unicode__(self):
        return u'Заявка на имя: %s, телефон: %s' % (self.name, self.phone)

    def performed_at(self):
        pass

    def send_admin_mail(self):
        mail_title_msg = u'На nadomofone.ru оставлена заявка'
        email = None
        if self.city:
            setup = get_object_or_None(Setup, city=self.city)
            if setup and setup.email:
                email = setup.email
        if not email:
            setup = Setup.objects.filter(city__isnull=True).first()
            if setup and setup.email:
                email = setup.email
        if email:
            if self.city:
                message = u'Имя: %s\nТелефон: %s\nГород: %s' % (self.name, self.phone, self.city)
            else:
                message = u'Имя: %s\nТелефон: %s\n' % (self.name, self.phone)
            send_mail(
                mail_title_msg,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email, ]
            )
        return False


@receiver(post_save, sender=Ticket)
def send_ticket_notify(sender, created, **kwargs):
    ticket = kwargs['instance']
    if created:
        ticket.send_admin_mail()
