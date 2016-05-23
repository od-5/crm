# coding=utf-8
import datetime
from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.urlresolvers import reverse
from django.db import models
from pytils.translit import slugify
import core.geotagging as api
from core.models import User

__author__ = 'alexy'

api_key = settings.YANDEX_MAPS_API_KEY


class City(models.Model):
    class Meta:
        verbose_name = u'Город'
        verbose_name_plural = u'Города'
        app_label = 'city'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('city:update', args=(self.pk,))

    def porch_count(self):
        """
        Метод возвращает количество подъездов города
        """
        count = 0
        for surface in self.surface_set.all():
            count += surface.porch_count()
        return count

    def surface_count(self):
        """
        Метод возвращает колиечество стендов, размещённых в городе.
        Количество стендов = Количество домов * количество подъездов в доме
        Рекламная поверхность - дом, для которого созданы подъезды.
        """
        count = 0
        for surface in self.surface_set.all():
            count += surface.porch_count()
        return count

    def save(self, *args, **kwargs):
        address = u'город %s' % self.name
        pos = api.geocode(api_key, address)
        self.coord_x = float(pos[0])
        self.coord_y = float(pos[1])
        if not self.slug:
            self.slug = slugify(self.name)
        super(City, self).save()

    name = models.CharField(max_length=100, verbose_name=u'Город')
    moderator = models.ForeignKey(to=User, blank=True, null=True, verbose_name=u'Модератор')
    contract_number = models.CharField(max_length=100, blank=True, null=True, verbose_name=u'Номер договора')
    contract_date = models.DateField(blank=True, null=True, verbose_name=u'Договор от')
    coord_x = models.DecimalField(max_digits=8, decimal_places=6, blank=True, null=True, verbose_name=u'Ширина')
    coord_y = models.DecimalField(max_digits=8, decimal_places=6, blank=True, null=True, verbose_name=u'Долгота')
    slug = models.SlugField(verbose_name=u'url имя поддомена', blank=True, null=True, max_length=50)


@receiver(post_save, sender=City)
def send_notify_to_admin(sender, created, **kwargs):
    if created:
        try:
            subject = u'Добавлен новый город %s, на сайте nadomofone.ru' % kwargs['instance'].name
            message = subject + u'\n URL для поддомена: %s' % kwargs['instance'].slug
            recepients = [admin[1] for admin in settings.ADMINS]
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                recepients
            )
        except:
            pass


class Area(models.Model):
    class Meta:
        verbose_name = u'Район'
        verbose_name_plural = u'Районы'
        app_label = 'city'

    def __unicode__(self):
        return self.name

    city = models.ForeignKey(to=City, verbose_name=u'Город')
    name = models.CharField(max_length=100, verbose_name=u'Название')


class Street(models.Model):
    class Meta:
        verbose_name = u'Улица'
        verbose_name_plural = u'Улицы'
        app_label = 'city'

    def __unicode__(self):
        if Street.objects.filter(city=self.city, name=self.name).count() > 1:
            return u'%s (%s)' % (self.name, self.area.name)
        return self.name

    city = models.ForeignKey(to=City, verbose_name=u'Город')
    area = models.ForeignKey(to=Area, verbose_name=u'Район')
    name = models.CharField(max_length=256, verbose_name=u'Название улицы')


class ManagementCompany(models.Model):
    class Meta:
        verbose_name = u'Управляющая компания'
        verbose_name_plural = u'Управляющие компании'
        app_label = 'city'

    def __unicode__(self):
        return u'г. %s, %s' % (self.city.name, self.name)

    def get_absolute_url(self):
        return reverse('city:management-company-update', args=(self.pk,))

    city = models.ForeignKey(to=City, verbose_name=u'Город')
    name = models.CharField(verbose_name=u'Название', max_length=255)
    leader_function = models.CharField(verbose_name=u'Должность руководители', max_length=255, blank=True, null=True)
    leader_name = models.CharField(verbose_name=u'ФИО руководители', max_length=255, blank=True, null=True)
    phone = models.CharField(verbose_name=u'Контактный телефон', max_length=20, blank=True, null=True)


class Surface(models.Model):
    class Meta:
        verbose_name = u'Поверхность'
        verbose_name_plural = u'Поверхности'
        app_label = 'city'

    def __unicode__(self):
        return u'г.%s %s %s' % (self.city.name, self.street.name, self.house_number)

    def get_current_client(self):
        try:
            today = datetime.datetime.today()
            return self.clientordersurface_set.select_related().filter(clientorder__date_start__lte=today, clientorder__date_end__gte=today).first().clientorder.client.legal_name
        except:
            return None

    def get_absolute_url(self):
        return reverse('surface:update', args=(self.pk,))
        # return '/city/surface/'

    def porch_count(self):
        return self.porch_set.all().count()

    def porch_list(self):
        return ', '.join([str(porch.number) for porch in self.porch_set.all()])

    def all_porch_damaged(self):
        count = self.porch_count()
        for porch in self.porch_set.all():
            count -= porch.is_broken
        return not count

    def damaged(self):
        for porch in self.porch_set.all():
            if porch.damaged():
                return True
        else:
            return False

    def save(self, *args, **kwargs):
        if not self.release_date:
            self.release_date = datetime.date.today() - datetime.timedelta(days=1)
        address = u'город %s %s %s' % (self.city.name, self.street.name, self.house_number)
        try:
            pos = api.geocode(api_key, address)
            self.coord_x = float(pos[0])
            self.coord_y = float(pos[1])
        except:
            pass
        super(Surface, self).save()

    city = models.ForeignKey(to=City, verbose_name=u'Город')
    street = models.ForeignKey(to=Street, verbose_name=u'Улица')
    house_number = models.CharField(max_length=50, verbose_name=u'Номер дома')
    management = models.ForeignKey(to=ManagementCompany, verbose_name=u'Управляющая контора', blank=True, null=True)
    coord_x = models.DecimalField(max_digits=8, decimal_places=6, blank=True, null=True, verbose_name=u'Ширина')
    coord_y = models.DecimalField(max_digits=8, decimal_places=6, blank=True, null=True, verbose_name=u'Долгота')
    free = models.BooleanField(default=True)
    has_broken = models.BooleanField(default=False, verbose_name=u'Есть повреждения')
    full_broken = models.BooleanField(default=False, verbose_name=u'Все стенды повреждены')
    release_date = models.DateField(blank=True, null=True, verbose_name=u'Дата освобождения поверхности')


class Porch(models.Model):
    class Meta:
        verbose_name = u'Подъезд'
        verbose_name_plural = u'Подъезды'
        app_label = 'city'
        ordering = ['number', ]

    def __unicode__(self):
        return u'подъезд № %s' % self.number

    def save(self, *args, **kwargs):
        """
        Если есть какие либо повреждения - стенд считается сломаным
        и для него может быть поставлена только задача на ремонт.
        Для поверхности, устанавливается флаг "has_broken" в True, если у подъезда есть повреждения.
        """
        if self.damaged():
            self.is_broken = True
            # surface = Surface.objects.get(pk=self.surface.id)
            # surface.has_broken = True
            # surface.save()
        else:
            self.is_broken = False
            # surface = Surface.objects.get(pk=self.surface.id)
            # surface.has_broken = False
            # surface.save()
        super(Porch, self).save()
        # todo: если что - искать неполадки с сохранением подъезда здесь!
        surface = Surface.objects.get(pk=self.surface.id)
        if surface.damaged():
            surface.has_broken = True
        else:
            surface.has_broken = False
        if surface.all_porch_damaged():
            surface.full_broken = True
        else:
            surface.full_broken = False
        surface.save()

    def damaged(self):
        """
        Метод возвращает True, если стенд на подъезде имеет хотя бы одно повреждение.
        Если стенд цел - возвращает False.
        """
        if self.broken_shield or self.broken_gib or self.no_glass or self.replace_glass or self.against_tenants or self.no_social_info:
            return True
        else:
            return False

    surface = models.ForeignKey(to=Surface, verbose_name=u'Рекламная поверхность')
    number = models.PositiveSmallIntegerField(verbose_name=u'Номер подъезда')
    broken_shield = models.BooleanField(verbose_name=u'Щит сломан', default=False)
    broken_gib = models.BooleanField(verbose_name=u'Сломана прижимная планка', default=False)
    no_glass = models.BooleanField(verbose_name=u'Отсутствует защитное стекло', default=False)
    replace_glass = models.BooleanField(verbose_name=u'Заменить защитное стекло', default=False)
    against_tenants = models.BooleanField(verbose_name=u'Жильцы против', default=False)
    no_social_info = models.BooleanField(verbose_name=u'Отсутствует социальная информация', default=False)
    is_broken = models.BooleanField(verbose_name=u'Стенд поломан', default=False)
