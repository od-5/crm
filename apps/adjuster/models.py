# coding=utf-8
from django.core.urlresolvers import reverse
from django.db import models
from django.conf import settings
from imagekit.models import ImageSpecField
from pilkit.processors import SmartResize
from core.files import UploadTo, upload_to
from apps.city.models import City, Surface, Porch
from core.models import User

__author__ = 'alexy'


class Adjuster(models.Model):
    class Meta:
        verbose_name = u'Монтажник'
        verbose_name_plural = u'Монтажники'
        app_label = 'adjuster'

    def __unicode__(self):
        return self.user.get_full_name()

    def get_absolute_url(self):
        return reverse('adjuster:change', args=(self.pk, ))

    user = models.OneToOneField(to=User, verbose_name=u'Пользователь')
    city = models.ForeignKey(to=City, verbose_name=u'Город')
    cost_mounting = models.PositiveIntegerField(verbose_name=u'Оплата за монтаж, руб', blank=True, null=True)
    cost_change = models.PositiveIntegerField(verbose_name=u'Оплата за замену, руб', blank=True, null=True)
    cost_repair = models.PositiveIntegerField(verbose_name=u'Оплата за ремонт, руб', blank=True, null=True)
    cost_dismantling = models.PositiveIntegerField(verbose_name=u'Оплата за демонтаж, руб', blank=True, null=True)


class SurfacePhoto(models.Model):
    class Meta:
        verbose_name = u'Фотография'
        verbose_name_plural = u'Фотографии'
        app_label = 'adjuster'

    def __unicode__(self):
        return u'%s подъезд № %s' % (self.porch.surface, self.porch)

    def address(self):
        return self.porch.surface

    def save(self, *args, **kwargs):
        if self.porch.damaged():
            self.is_broken = True
            print 'damaged'
        else:
            self.is_broken = False
            print 'not damaged'
        print 'save'
        super(SurfacePhoto, self).save()

    porch = models.ForeignKey(to=Porch, verbose_name=u'Подъезд')
    adjuster = models.ForeignKey(to=Adjuster, blank=True, null=True, verbose_name=u'Монтажник')
    date = models.DateField(verbose_name=u'Дата фотографии')
    image = models.ImageField(verbose_name=u'Изображение', upload_to=upload_to)
    image_resize = ImageSpecField(
        [SmartResize(*settings.SURFACE_THUMB_SIZE)], source='image', format='JPEG', options={'quality': 94}
    )
    is_broken = models.BooleanField(default=False)


class AdjusterTask(models.Model):
    class Meta:
        verbose_name = u'Монтажник'
        verbose_name_plural = u'Монтажники'
        app_label = 'adjuster'
        ordering = ['-date', ]

    def __unicode__(self):
        return u'Задача ID №:%d' % self.id

    def get_absolute_url(self):
        return reverse('adjustertask:update', args=(self.id, ))

    def get_porch_count(self):
        porch_count = 0
        if self.adjustertasksurface_set.all() > 0:
            for i in self.adjustertasksurface_set.all():
                porch_count += i.surface.porch_count()
        return porch_count

    def get_total_cost(self):
        if self.type == 0 and self.adjuster.cost_mounting:
            cost = self.adjuster.cost_mounting
        elif self.type == 1 and self.adjuster.cost_change:
            cost = self.adjuster.cost_change
        elif self.type == 2 and self.adjuster.cost_repair:
            cost = self.adjuster.cost_repair
        elif self.type == 3 and self.adjuster.cost_dismantling:
            cost = self.adjuster.cost_dismantling
        else:
            cost = 0
        return cost * self.adjustertasksurface_set.count()

    TYPE_CHOICES = (
        (0, u'Монтаж новой конструкции'),
        (1, u'Замена'),
        (2, u'Ремонт стенда'),
        (3, u'Демонтаж стенда'),
    )

    adjuster = models.ForeignKey(to=Adjuster, verbose_name=u'Монтажник')
    type = models.PositiveSmallIntegerField(verbose_name=u'Вид работы', choices=TYPE_CHOICES)
    date = models.DateField(verbose_name=u'Дата проведения работы')
    comment = models.TextField(verbose_name=u'Комментарий', blank=True, null=True)


class AdjusterTaskSurface(models.Model):
    class Meta:
        verbose_name = u'Поверхность для задачи'
        verbose_name_plural = u'Поверхности для задачи'
        app_label = 'adjuster'

    def __unicode__(self):
        return u'#%d Задача для монтажника %s. Дата: %s' % (self.id, self.adjustertask.adjuster.user.get_full_name, self.adjustertask.date)

    adjustertask = models.ForeignKey(to=AdjusterTask, verbose_name=u'Задача')
    surface = models.ForeignKey(to=Surface, verbose_name=u'Поверхность')
