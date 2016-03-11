# coding=utf-8
import datetime
from django.conf import settings
import datetime
from django.utils.timezone import utc
from django.core.urlresolvers import reverse
from django.db import models
from apps.city.models import City, Surface
from core.files import upload_to
from core.models import User
from apps.manager.models import Manager

__author__ = 'alexy'


class Client(models.Model):
    class Meta:
        verbose_name = u'Клиент'
        verbose_name_plural = u'Клиенты'
        app_label = 'client'

    def __unicode__(self):
        return self.legal_name

    user = models.OneToOneField(to=User, verbose_name=u'Пользователь')
    city = models.ForeignKey(to=City, verbose_name=u'Город')
    manager = models.ForeignKey(to=Manager, verbose_name=u'Менеджер', blank=True, null=True)
    legal_name = models.CharField(max_length=256, blank=True, null=True, verbose_name=u'Юридическое название')
    actual_name = models.CharField(max_length=256, blank=True, null=True, verbose_name=u'Фактичексое название')
    inn = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'ИНН')
    kpp = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'КПП')

    ogrn = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'ОГРН')
    bank = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'Банк')
    bik = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'БИК')
    account = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'Расчётный счёт')
    account_cor = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'Кор. счёт')
    signer_post_dec = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'должность подписанта')
    signer_name_dec = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'имя подписанта')
    signer_doc_dec = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'действует на основании')

    legal_address = models.TextField(verbose_name=u'Физический адрес', blank=True, null=True)
    leader = models.CharField(max_length=100, blank=True, null=True, verbose_name=u'Руководитель')
    leader_function = models.CharField(max_length=100, blank=True, null=True, verbose_name=u'Должность руководителя')
    work_basis = models.CharField(max_length=256, blank=True, null=True, verbose_name=u'Основание для работы')


class ClientOrder(models.Model):
    class Meta:
        verbose_name = u'Заказ'
        verbose_name_plural = u'Заказы'
        app_label = 'client'
        ordering = ['-date_start', ]

    def __unicode__(self):
        if self.date_end:
            return u'Заказ %s - %s ' % (self.date_start, self.date_end)
        else:
            return u'Заказ  %s - <дата окончания не указана> ' % self.date_start

    def delete(self, *args, **kwargs):
        """
        При удалении заказа, для всех заказанных поверхностей автоматически устанавливется флаг "Поверхность свободна",
        т.е. доступна для заказа
        """
        release_date = datetime.datetime.utcnow().replace(tzinfo=utc) - datetime.timedelta(days=1)
        if self.clientordersurface_set.all():
            for c_surface in self.clientordersurface_set.all():
                surface = Surface.objects.get(pk=c_surface.surface.id)
                surface.free = True
                surface.release_date = release_date.date()
                surface.save()
        super(ClientOrder, self).delete()

    def stand_count(self):
        if self.clientordersurface_set.all():
            total = 0
            for i in self.clientordersurface_set.all():
                total += i.porch_count()
            return total
        else:
            return 0

    client = models.ForeignKey(to=Client, verbose_name=u'Клиент')
    date_start = models.DateField(verbose_name=u'Дата начала размещения')
    date_end = models.DateField(verbose_name=u'Дата окончания размещения')
    is_closed = models.BooleanField(verbose_name=u'Заказ закрыт', default=False)
#     todo: продумать флаг "Заказ закрыт"


class ClientOrderSurface(models.Model):
    class Meta:
        verbose_name = u'Пункт заказа'
        verbose_name_plural = u'Пункты заказа'
        app_label = 'client'

    def __unicode__(self):
        return u'%s %s ' % (self.surface.street.name, self.surface.house_number)

    def porch_count(self):
        if self.surface.porch_set.all():
            return self.surface.porch_set.all().count()
        else:
            return 0

    def delete(self, *args, **kwargs):
        release_date = datetime.datetime.utcnow().replace(tzinfo=utc) - datetime.timedelta(days=1)
        surface = Surface.objects.get(pk=self.surface.id)
        surface.free = True
        surface.release_date = release_date.date()
        surface.save()
        super(ClientOrderSurface, self).delete()

    clientorder = models.ForeignKey(to=ClientOrder, verbose_name=u'Заказ')
    surface = models.ForeignKey(to=Surface, verbose_name=u'Рекламная поверхность')


class ClientJournal(models.Model):
    class Meta:
        verbose_name = u'Покупка'
        verbose_name_plural = u'Покупки'
        app_label = 'client'

    def __unicode__(self):
        return u'Покупка на дату %s' % self.created

    def stand_count(self):
        stand_count = 0
        for clientorder in self.clientorder.all():
            stand_count += clientorder.stand_count()
        return stand_count

    def total_cost(self):
        cost = self.cost
        if self.add_cost:
            add_cost = self.add_cost
        else:
            add_cost = 0
        if self.discount:
            discount = self.discount
        else:
            discount = 0
        sum = ((cost*(1+add_cost*0.01))*(1+discount*0.01)) * self.stand_count()
        return round(sum, 2)

    client = models.ForeignKey(to=Client, verbose_name=u'клиент')
    clientorder = models.ManyToManyField(to=ClientOrder, verbose_name=u'заказ клиента')
    cost = models.PositiveIntegerField(verbose_name=u'Цена за стенд, руб')
    add_cost = models.PositiveIntegerField(verbose_name=u'Наценка, %', blank=True, null=True)
    discount = models.PositiveIntegerField(verbose_name=u'Скидка, %', blank=True, null=True)
    created = models.DateField(auto_now_add=True, verbose_name=u'Дата создания')


class ClientMaket(models.Model):
    class Meta:
        verbose_name = u'Макет'
        verbose_name_plural = u'Макеты'
        app_label = 'client'
        ordering = ['-date']

    def __unicode__(self):
        return self.name

    client = models.ForeignKey(to=Client, verbose_name=u'Клиент')
    name = models.CharField(max_length=256, verbose_name=u'Название')
    file = models.FileField(verbose_name=u'Файл макета', upload_to=upload_to)
    date = models.DateField(verbose_name=u'Дата размещения макета')
