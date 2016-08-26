# coding=utf-8
from django.db import models
from apps.city.models import City
from core.models import User

__author__ = 'alexy'


class Superviser(models.Model):
    class Meta:
        verbose_name = u'Информация о супервайзере'
        verbose_name_plural = u'Информация о супервайзерах'
        app_label = 'superviser'

    def __unicode__(self):
        return self.superviser.get_full_name()

    def city_id_list(self):
        try:
            return [int(city.id) for city in self.city.all()]
        except:
            return None

    def moderator_id_list(self):
        if self.city.all():
            moderator_list = []
            for city in self.city.all():
                if city.moderator and city.moderator.id not in moderator_list:
                    moderator_list.append(int(city.moderator.id))
            return moderator_list
        else:
            return None

    superviser = models.OneToOneField(to=User, verbose_name=u'Супервайзер')
    city = models.ManyToManyField(to=City, verbose_name=u'Города', blank=True, null=True)
