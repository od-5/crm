# coding=utf-8
from PIL import Image
from django.core.files import File
from django.urls import reverse
from django.db import models
from django.conf import settings
from imagekit.models import ImageSpecField
from pilkit.processors import SmartResize
from django.db.models.signals import post_save
from django.dispatch import receiver
from pytils.translit import slugify
from core.files import UploadTo, upload_to, surfacephoto_upload
from apps.city.models import City, Surface, Porch
from core.models import User

__author__ = 'alexy'


class AdjusterModelManager(models.Manager):
    def get_qs(self, user):
        if user.type == 1:
            qs = self.model.objects.all()
        elif user.type == 6:
            qs = self.model.objects.filter(city__in=user.superviser.city.all())
        elif user.type == 2:
            qs = self.model.objects.filter(city__moderator=user)
        elif user.type == 5:
            qs = self.model.objects.filter(city__moderator=user.manager.moderator)
        else:
            qs = self.model.objects.none()
        return qs


class Adjuster(models.Model):
    user = models.OneToOneField(on_delete=models.CASCADE, to=User, verbose_name=u'Пользователь')
    city = models.ForeignKey(on_delete=models.CASCADE, to=City, verbose_name=u'Город')
    cost_mounting = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=u'Оплата за монтаж, руб',
                                        blank=True, null=True)
    cost_change = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=u'Оплата за замену, руб',
                                      blank=True, null=True)
    cost_repair = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=u'Оплата за ремонт, руб',
                                      blank=True, null=True)
    cost_dismantling = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=u'Оплата за демонтаж, руб',
                                           blank=True, null=True)
    coord_x = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name=u'Ширина')
    coord_y = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name=u'Долгота')

    objects = AdjusterModelManager()

    class Meta:
        verbose_name = u'Монтажник'
        verbose_name_plural = u'Монтажники'
        app_label = 'adjuster'

    def __unicode__(self):
        return self.user.get_full_name()

    def __str__(self):
        return self.__unicode__()

    def get_absolute_url(self):
        return reverse('adjuster:change', args=(self.pk,))


class SurfacePhoto(models.Model):
    class Meta:
        verbose_name = u'Фотография'
        verbose_name_plural = u'Фотографии'
        app_label = 'adjuster'
        ordering = ['-id', ]

    def __unicode__(self):
        return u'%s д.%s п.%s' % (self.porch.surface.street.name, self.porch.surface.house_number, self.porch.number)

    def __str__(self):
        return self.__unicode__()

    def address(self):
        return self.porch.surface

    def image_exists(self):
        return self.image.storage.exists(self.image.name)

    def save(self, *args, **kwargs):
        super(SurfacePhoto, self).save()

    porch = models.ForeignKey(on_delete=models.CASCADE, to=Porch, verbose_name=u'Подъезд')
    adjuster = models.ForeignKey(on_delete=models.CASCADE, to=Adjuster, blank=True, null=True, verbose_name=u'Монтажник')
    date = models.DateTimeField(verbose_name=u'Дата фотографии')
    image = models.ImageField(verbose_name=u'Изображение', upload_to=surfacephoto_upload)
    image_resize = ImageSpecField(
        [SmartResize(*settings.SURFACE_THUMB_SIZE)], source='image', format='JPEG', options={'quality': 94}
    )
    is_broken = models.BooleanField(default=False, verbose_name=u'Поломка')


@receiver(models.signals.pre_delete, sender=SurfacePhoto)
def delete_old_image_resize(sender, instance, **kwargs):
    try:
        file = instance.image_resize.file
        cache_backend = instance.image_resize.cachefile_backend
        cache_backend.cache.delete(cache_backend.get_key(file))
        instance.image_resize.storage.delete(file)
    except:
        pass
    instance.image.delete()


class AdjusterTask(models.Model):
    class Meta:
        verbose_name = u'Монтажник'
        verbose_name_plural = u'Монтажники'
        app_label = 'adjuster'
        ordering = ['-date', ]

    def __unicode__(self):
        return u'Задача ID №:%d' % self.id

    def __str__(self):
        return self.__unicode__()

    def get_api_url(self):
        return reverse('api:task_detail', args=(self.id,))

    def get_absolute_url(self):
        return reverse('adjustertask:update', args=(self.id,))

    def get_city_name(self):
        return self.adjuster.city.name

    def get_surface_count(self):
        return self.adjustertasksurface_set.count()

    def get_closed_surface_count(self):
        return self.adjustertasksurface_set.filter(is_closed=True).count()

    def get_porch_dict(self):
        porch_dict = {}
        for ats in self.adjustertasksurface_set.prefetch_related('adjustertasksurfaceporch_set').all():
            for atsp in ats.adjustertasksurfaceporch_set.all():
                if atsp.id not in porch_dict:
                    porch_dict.update({atsp.id: atsp.complete})
        return porch_dict

    def get_porch_count(self):
        """
        Метод, возвращающий количество подъездов/стендов, входящих в задачу
        """
        # return AdjusterTaskSurfacePorch.objects.filter(adjustertasksurface__adjustertask=self).count()
        return len(self.get_porch_dict())

    def get_closed_porch_count(self):
        """
        Метод, возвращающий количество выполненных подъездов/стендов, входящих в задачу
        """
        # return AdjusterTaskSurfacePorch.objects.filter(adjustertasksurface__adjustertask=self, is_closed=True).count()
        count = 0
        porch_dict = self.get_porch_dict()
        for i in porch_dict:
            if porch_dict[i]:
                count += 1
        return count

    def get_actual_cost(self):
        """
        Метод, возвращающий цену за фактичечески выполненную на данный момент работу.
        Кол-во выполненных стендов * цена работы по подному стенду
        """
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
        sum = float(cost) * self.get_closed_porch_count()
        return round(sum, 2)

    def get_total_cost(self):
        """
        Метод, возвращающий полную стоимость работы.
        Кол-во стендов в задаче * цена работы по одному стенду
        """
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
        sum = float(cost) * self.get_porch_count()
        return round(sum, 2)

    def get_process(self):
        """
        Метод, возвращающий % выполнения задачи.
        Кол-во выполненных стендов * 100 / кол-во стендов в задаче
        """
        porch_count = self.get_porch_count()
        closed_proch_count = self.get_closed_porch_count()
        if porch_count == 0:
            return 0
        else:
            return closed_proch_count * 100 / porch_count

    TYPE_CHOICES = (
        (0, u'Монтаж новой конструкции'),
        (1, u'Замена'),
        (2, u'Ремонт стенда'),
        (3, u'Демонтаж стенда'),
    )

    adjuster = models.ForeignKey(on_delete=models.CASCADE, to=Adjuster, verbose_name=u'Монтажник')
    type = models.PositiveSmallIntegerField(verbose_name=u'Вид работы', choices=TYPE_CHOICES)
    date = models.DateField(verbose_name=u'Дата задачи')
    comment = models.TextField(verbose_name=u'Комментарий', blank=True, null=True)
    is_closed = models.BooleanField(verbose_name=u'Выполнено', default=False)
    sent = models.BooleanField(verbose_name=u'Отправлено', default=False)


@receiver(post_save, sender=AdjusterTask)
def write_ats(sender, created, **kwargs):
    """
    Принудительное закрытие всех адресов в задаче при установка чекбокса ВЫПОЛНЕНО.
    """
    task = kwargs['instance']
    if task.is_closed:
        for ats in task.adjustertasksurface_set.filter(is_closed=False):
            for atsp in ats.adjustertasksurfaceporch_set.filter(is_closed=False):
                atsp.is_closed = True
                atsp.complete = False
                atsp.save()
            ats.is_closed = True
            ats.complate = False
            ats.save()


class AdjusterTaskSurface(models.Model):
    class Meta:
        verbose_name = u'Поверхность для задачи'
        verbose_name_plural = u'Поверхности для задачи'
        app_label = 'adjuster'

    def __unicode__(self):
        return u'поверхность %s' % self.surface

    def __str__(self):
        return self.__unicode__()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(AdjusterTaskSurface, self).save()
        if self.adjustertask.get_closed_surface_count() == self.adjustertask.get_surface_count():
            at = AdjusterTask.objects.get(id=self.adjustertask.id)
            at.is_closed = True
            at.save()

    def get_api_url(self):
        return reverse('api:tasksurface_detail', args=(self.id,))

    def get_coord(self):
        return [self.surface.coord_y, self.surface.coord_x]

    def get_address(self):
        return u'%s, %s, д. %s' % (self.surface.street.area.name, self.surface.street.name, self.surface.house_number)

    def get_porch_count(self):
        """
        Количество подъездов по данному адресу
        """
        return self.adjustertasksurfaceporch_set.count()

    def get_closed_porch_count(self):
        """
        Количество выполненных подъездов по данному адресу
        """
        count = 0
        for atsp in self.adjustertasksurfaceporch_set.all():
            if atsp.is_closed and atsp.complete:
                count += 1
        return count
        # return self.adjustertasksurfaceporch_set.filter(is_closed=True, complete=True).count()

    adjustertask = models.ForeignKey(on_delete=models.CASCADE, to=AdjusterTask, verbose_name=u'Задача')
    surface = models.ForeignKey(on_delete=models.CASCADE, to=Surface, verbose_name=u'Поверхность')
    is_closed = models.BooleanField(verbose_name=u'Выполнено', default=False)


class AdjusterTaskSurfacePorch(models.Model):
    class Meta:
        verbose_name = u'Подъезд по задаче'
        verbose_name_plural = u'Подъезды па задаче'
        app_label = 'adjuster'

    def __unicode__(self):
        return u'№ %s' % self.porch.number

    def __str__(self):
        return self.__unicode__()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(AdjusterTaskSurfacePorch, self).save()
        if self.adjustertasksurface.get_closed_porch_count() == self.adjustertasksurface.get_porch_count():
            ats = AdjusterTaskSurface.objects.get(id=self.adjustertasksurface.id)
            ats.is_closed = True
            ats.save()

    def porch_number(self):
        return self.porch.number

    def broken_shield(self):
        return self.porch.broken_shield

    def broken_gib(self):
        return self.porch.broken_gib

    def no_glass(self):
        return self.porch.no_glass

    def replace_glass(self):
        return self.porch.replace_glass

    def against_tenants(self):
        return self.porch.against_tenants

    def no_social_info(self):
        return self.porch.no_social_info

    adjustertasksurface = models.ForeignKey(on_delete=models.CASCADE, to=AdjusterTaskSurface, verbose_name=u'Поверхность для задачи')
    porch = models.ForeignKey(on_delete=models.CASCADE, to=Porch, verbose_name=u'Подъезд поверхности для задачи')
    is_closed = models.BooleanField(verbose_name=u'Выполнено', default=False)
    complete = models.BooleanField(verbose_name=u'Работы выполнены', default=False)
