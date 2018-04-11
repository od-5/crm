# coding=utf-8
from django.core.urlresolvers import reverse
from django.db import models
from core.models import User

__author__ = 'alexy'


class ManagerModelManager(models.Manager):

    @staticmethod
    def get_qs(user):
        qs = Manager.objects.none()
        if user.type == 1:
            qs = Manager.objects.all()
        elif user.type == 2:
            qs = Manager.objects.filter(moderator=user)
        elif user.type == 5:
            qs = Manager.objects.filter(moderator=user.manager.moderator)
        elif user.type == 6:
            qs = Manager.objects.filter(moderator__in=user.superviser.moderator_id_list())
        return qs


class Manager(models.Model):
    user = models.OneToOneField(to=User, verbose_name=u'Пользователь')
    moderator = models.ForeignKey(to=User, verbose_name=u'Модератор', related_name='moderator')
    leader = models.BooleanField(verbose_name=u'Руководитель группы', default=False)

    objects = ManagerModelManager()

    class Meta:
        verbose_name = u'Менеджер'
        verbose_name_plural = u'Менеджеры'
        app_label = 'manager'

    def __unicode__(self):
        return self.user.get_full_name()

    def get_absolute_url(self):
        return reverse('manager:update', args=(self.pk, ))


