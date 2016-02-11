# coding=utf-8
from django.core.urlresolvers import reverse
from django.db import models
from apps.city.models import City
from apps.manager.models import Manager

__author__ = 'alexy'


class IncomingClient(models.Model):
    class Meta:
        verbose_name = u'Клиент'
        verbose_name_plural = u'Клиенты'
        app_label = 'incoming'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('incoming:update', args=(self.pk, ))

    manager = models.ForeignKey(to=Manager, verbose_name=u'Менеджер')
    name = models.CharField(verbose_name=u'Название', max_length=255)
    city = models.ForeignKey(to=City, verbose_name=u'Город')
    kind_of_activity = models.CharField(verbose_name=u'Вид деятельности', max_length=255, blank=True, null=True)
    actual_address = models.CharField(verbose_name=u'Фактический адрес', max_length=255, blank=True, null=True)
    phone = models.CharField(verbose_name=u'Телефон', blank=True, null=True, max_length=20)
    fax = models.CharField(verbose_name=u'Телефон\Факс', blank=True, null=True, max_length=20)
    mobile_phone = models.CharField(verbose_name=u'Мобильный телефон', blank=True, null=True,  max_length=20)
    email = models.EmailField(verbose_name=u'Email', blank=True, null=True,  max_length=30)
    site = models.CharField(verbose_name=u'Сайт', blank=True, null=True,  max_length=100)
    leader = models.CharField(verbose_name=u'ФИО руководителя', blank=True, null=True,  max_length=2550)


class IncomingTask(models.Model):
    class Meta:
        verbose_name = u'Задача'
        verbose_name_plural = u'Задачи'
        app_label = 'incoming'

    def __unicode__(self):
        return self.get_type_display

    def get_absolute_url(self):
        return reverse('incoming:task-update', args=(self.pk, ))

    TASK_TYPE_CHOICES = (
        (0, u'Тип задачи 1'),
        (1, u'Тип задачи 1'),
        (2, u'Тип задачи 1'),
        (3, u'Тип задачи 1'),
    )

    manager = models.ForeignKey(to=Manager, verbose_name=u'Менеджер')
    incomingclient = models.ForeignKey(to=IncomingClient, verbose_name=u'Входящий клиент')
    type = models.PositiveIntegerField(choices=TASK_TYPE_CHOICES, verbose_name=u'Тип задачи')
    date = models.DateField(verbose_name=u'Дата')
    comment = models.TextField(verbose_name=u'Комментарий', blank=True, null=True)