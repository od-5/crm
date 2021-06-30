# coding=utf-8
import datetime
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Sum
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.urls import reverse, reverse_lazy
from django.db import models
from pytils.translit import slugify
import core.geotagging as api
from core.models import User

__author__ = 'alexy'

api_key = settings.YANDEX_MAPS_API_KEY


class CityModelManager(models.Manager):
    def get_qs(self, user):
        if user.type == 1:
            qs = self.model.objects.all()
        elif user.type == 2:
            qs = user.city_set.all()
        elif user.type == 3:
            qs = self.model.objects.filter(id=user.client.city.id)
        elif user.type == 6:
            qs = user.superviser.city.all()
        elif user.type == 5:
            qs = user.manager.moderator.city_set.all()
        else:
            qs = self.model.objects.none()
        return qs


class City(models.Model):
    TIME_CHOICES = tuple((i, i) for i in range(-12, 13))

    name = models.CharField(max_length=100, verbose_name=u'Город')
    moderator = models.ForeignKey(on_delete=models.CASCADE, to=User, limit_choices_to={'type': 2}, blank=True, null=True,
                                  verbose_name=u'Модератор')
    contract_number = models.CharField(max_length=100, blank=True, null=True, verbose_name=u'Номер договора')
    contract_date = models.DateField(blank=True, null=True, verbose_name=u'Договор от')
    coord_x = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name=u'Ширина')
    coord_y = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name=u'Долгота')
    slug = models.SlugField(verbose_name=u'url имя поддомена', blank=True, null=True, max_length=50)
    timezone = models.SmallIntegerField(verbose_name=u'Часовой пояс', default=3, choices=TIME_CHOICES)
    # stand_total_count = models.IntegerField(blank=True, null=True, default=0)

    objects = CityModelManager()

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
        return Porch.objects.select_related('surface__city').filter(surface__city=self).count()

    def surface_count(self):
        """
        Метод возвращает колиечество стендов, размещённых в городе.
        Количество стендов = Количество домов * количество подъездов в доме
        Рекламная поверхность - дом, для которого созданы подъезды.
        """
        # count = self.surface_set.all().aggregate(Sum('porch_total_count'))['porch_total_count__sum'] or 0
        # return count
        return Porch.objects.select_related('surface__city').filter(surface__city=self).count()

    def save(self, *args, **kwargs):
        address = u'город %s' % self.name
        pos = api.geocode(api_key, address)
        self.coord_x = float(pos[0])
        self.coord_y = float(pos[1])
        if not self.slug:
            self.slug = slugify(self.name)
        # self.surfaces = self.surface_count()
        super(City, self).save()


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
    city = models.ForeignKey(on_delete=models.CASCADE, to=City, verbose_name=u'Город')
    name = models.CharField(max_length=100, verbose_name=u'Название')

    class Meta:
        verbose_name = u'Район'
        verbose_name_plural = u'Районы'
        app_label = 'city'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('city:area', args=(self.city.id,))


class Street(models.Model):
    city = models.ForeignKey(on_delete=models.CASCADE, to=City, verbose_name=u'Город')
    area = models.ForeignKey(on_delete=models.CASCADE, to=Area, verbose_name=u'Район')
    name = models.CharField(max_length=256, verbose_name=u'Название улицы')

    class Meta:
        verbose_name = u'Улица'
        verbose_name_plural = u'Улицы'
        app_label = 'city'

    def __unicode__(self):
        if self.city.street_set.filter(name=self.name).count() > 1:
        # if Street.objects.filter(city=self.city, name=self.name).count() > 1:
            return u'%s (%s)' % (self.name, self.area.name)
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('city:street', args=(self.city_id,))


class ManagementCompany(models.Model):
    class Meta:
        verbose_name = u'Управляющая компания'
        verbose_name_plural = u'Управляющие компании'
        app_label = 'city'

    def __unicode__(self):
        return u'г. %s, %s' % (self.city.name, self.name)

    def get_absolute_url(self):
        return reverse('city:management-company-update', args=(self.pk,))

    city = models.ForeignKey(on_delete=models.CASCADE, to=City, verbose_name=u'Город')
    name = models.CharField(verbose_name=u'Название', max_length=255)
    leader_function = models.CharField(verbose_name=u'Адрес и комментарии', max_length=455, blank=True, null=True)
    leader_name = models.CharField(verbose_name=u'ФИО руководители', max_length=255, blank=True, null=True)
    phone = models.CharField(verbose_name=u'Контактный телефон', max_length=40, blank=True, null=True)
    phones = models.TextField(verbose_name=u'Телефоны для docx файла в формате "Аварийка#3-30-23$Газ#3-30-22"',
                              blank=True, null=True)

    @property
    def doc_phones(self):
        data = []
        if self.phones and '$' in self.phones and '#' in 'self.phones':
            for phone in self.phones.split('$'):
                data.append({
                    'type': phone.split('#')[0],
                    'phone': phone.split('#')[1]
                })
        return data


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
            return self.clientordersurface_set.select_related().filter(
                clientorder__date_start__lte=today,
                clientorder__date_end__gte=today
            ).first().clientorder.client.legal_name
        except:
            return None

    def get_absolute_url(self):
        return reverse('surface:update', args=(self.pk,))
        # return '/city/surface/'

    def porch_count(self):
        return self.porch_set.count()

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
            self.release_date = datetime.date.today() - datetime.timedelta(days=30)
        # fixme: придумать как определять координаты только при создании и изменении через сайт
        address = u'город %s %s %s' % (self.city.name, self.street.name, self.house_number)
        try:
            pos = api.geocode(api_key, address)
            self.coord_x = float(pos[0])
            self.coord_y = float(pos[1])
        except:
            pass
        super(Surface, self).save()

    city = models.ForeignKey(on_delete=models.CASCADE, to=City, verbose_name=u'Город')
    street = models.ForeignKey(on_delete=models.CASCADE, to=Street, verbose_name=u'Улица')
    house_number = models.CharField(max_length=50, verbose_name=u'Номер дома')
    management = models.ForeignKey(on_delete=models.CASCADE, to=ManagementCompany, verbose_name=u'Управляющая контора', blank=True, null=True)
    coord_x = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name=u'Ширина')
    coord_y = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name=u'Долгота')
    free = models.BooleanField(default=True)
    has_broken = models.BooleanField(default=False, verbose_name=u'Есть повреждения')
    full_broken = models.BooleanField(default=False, verbose_name=u'Все стенды повреждены')
    release_date = models.DateField(blank=True, null=True, verbose_name=u'Дата освобождения поверхности')
    porch_total_count = models.IntegerField(blank=True, null=True, default=0)
    has_stand = models.BooleanField(default=False, verbose_name=u'Стенды установлены')
    floors = models.PositiveSmallIntegerField(verbose_name=u'Этажность', blank=True, null=True)
    apart_count = models.PositiveSmallIntegerField(verbose_name=u'Кол-во квартир', blank=True, null=True)


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

    surface = models.ForeignKey(on_delete=models.CASCADE, to=Surface, verbose_name=u'Рекламная поверхность')
    number = models.PositiveSmallIntegerField(verbose_name=u'Номер подъезда')
    broken_shield = models.BooleanField(verbose_name=u'Щит сломан', default=False)
    broken_gib = models.BooleanField(verbose_name=u'Сломана прижимная планка', default=False)
    no_glass = models.BooleanField(verbose_name=u'Отсутствует защитное стекло', default=False)
    replace_glass = models.BooleanField(verbose_name=u'Заменить защитное стекло', default=False)
    against_tenants = models.BooleanField(verbose_name=u'Жильцы против', default=False)
    no_social_info = models.BooleanField(verbose_name=u'Отсутствует социальная информация', default=False)
    is_broken = models.BooleanField(verbose_name=u'Стенд поломан', default=False)


class SurfaceDocTemplate(models.Model):
    docx = models.FileField(blank=True, null=True)

    def __unicode__(self):
        return 'Шаблон'


@receiver(post_save, sender=Porch)
def increment_porch_total_count(sender, created, **kwargs):
    surface = kwargs['instance'].surface
    if created:
        surface.porch_total_count += 1
        surface.save()


@receiver(post_delete, sender=Porch)
def decrement_porch_total_count(sender, **kwargs):
    surface = kwargs['instance'].surface
    surface.porch_total_count -= 1
    surface.save()
