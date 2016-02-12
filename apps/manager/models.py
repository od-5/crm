# coding=utf-8
from django.core.urlresolvers import reverse
from django.db import models
from core.models import User

__author__ = 'alexy'


class Manager(models.Model):
    class Meta:
        verbose_name = u'Менеджер'
        verbose_name_plural = u'Менеджеры'
        app_label = 'manager'

    def __unicode__(self):
        return self.user.get_full_name()

    def get_absolute_url(self):
        return reverse('manager:update', args=(self.pk, ))

    user = models.OneToOneField(to=User, verbose_name=u'Пользователь')
    moderator = models.ForeignKey(to=User, verbose_name=u'Модератор', related_name='moderator')
