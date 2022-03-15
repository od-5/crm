# coding=utf-8
import datetime
from django.conf import settings
import datetime

from django.db.models import Count
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils.timezone import utc
from django.urls import reverse
from django.db import models
from apps.city.models import City, Surface, Porch
from core.files import upload_to
from core.models import User
from apps.manager.models import Manager

__author__ = 'alexy'


class Client(models.Model):
    user = models.OneToOneField(on_delete=models.CASCADE, to=User, verbose_name=u'Пользователь')
    city = models.ForeignKey(on_delete=models.CASCADE, to=City, verbose_name=u'Город')
    manager = models.ForeignKey(on_delete=models.CASCADE, to=Manager, verbose_name=u'Менеджер', blank=True, null=True)
    legal_name = models.CharField(max_length=256, blank=True, null=True, verbose_name=u'Юридическое название')
    actual_name = models.CharField(max_length=256, blank=True, null=True, verbose_name=u'Фактическое название')
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
    photo_additional = models.PositiveIntegerField(default=0, blank=True, null=True,
                                                   verbose_name=u'накрутка к кол-ву фотографий')
    has_limit_surfaces = models.BooleanField('Использовать "Зону покрытия"', default=False)


    class Meta:
        verbose_name = u'Клиент'
        verbose_name_plural = u'Клиенты'
        app_label = 'client'
        ordering = ['-id']

    def __unicode__(self):
        return self.legal_name

    def __str__(self):
        return self.legal_name or self.actual_name or self.user.email


class ClientOrder(models.Model):
    client = models.ForeignKey(on_delete=models.CASCADE, to=Client, verbose_name=u'Клиент')
    date_start = models.DateField(verbose_name=u'Дата начала размещения')
    date_end = models.DateField(verbose_name=u'Дата окончания размещения')
    is_closed = models.BooleanField(verbose_name=u'Заказ закрыт', default=False)
    name = models.CharField(verbose_name=u'Название', blank=True, null=True, max_length=200)

    class Meta:
        verbose_name = u'Заказ'
        verbose_name_plural = u'Заказы'
        app_label = 'client'
        ordering = ['-date_start', ]

    def __unicode__(self):
        if self.name:
            return self.name
        if self.date_end:
            return u'Заказ %s - %s ' % (self.date_start, self.date_end)
        else:
            return u'Заказ  %s - <дата окончания не указана> ' % self.date_start

    def __str__(self):
        return self.__unicode__()

    def delete(self, *args, **kwargs):
        """
        При удалении заказа, для всех заказанных поверхностей автоматически устанавливется флаг "Поверхность свободна",
        т.е. доступна для заказа
        """
        release_date = datetime.datetime.utcnow().replace(tzinfo=utc) - datetime.timedelta(days=365)
        if self.clientordersurface_set.all():
            for c_surface in self.clientordersurface_set.all():
                surface = Surface.objects.get(pk=c_surface.surface.id)
                surface.free = True
                surface.release_date = release_date.date()
                surface.save()
        super(ClientOrder, self).delete()

    def stand_count(self):
        return Porch.objects.filter(surface__clientordersurface__clientorder=self).count()

    def clientordersurface_list(self):
        return (
            self.clientordersurface_set
            .select_related('surface', 'surface__street', 'surface__street__area', 'surface__management')
            .annotate(num_porch=Count('surface__porch'))
            .extra(select={'house_number_int': 'CAST(city_surface.house_number AS INTEGER)'})
            .order_by('surface__street__area', 'surface__street__name', 'house_number_int')
        )


class ClientOrderSurface(models.Model):
    clientorder = models.ForeignKey(on_delete=models.CASCADE, to=ClientOrder, verbose_name=u'Заказ')
    surface = models.ForeignKey(on_delete=models.CASCADE, to=Surface, verbose_name=u'Рекламная поверхность')

    class Meta:
        verbose_name = u'Пункт заказа'
        verbose_name_plural = u'Пункты заказа'
        app_label = 'client'

    def __unicode__(self):
        return u'%s %s ' % (self.surface.street.name, self.surface.house_number)

    def __str__(self):
        return self.__unicode__()

    def porch_count(self):
        if self.surface.porch_set.select_related().all():
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


class ClientJournalModelManager(models.Manager):
    def get_qs(self, user):
        if user.type == 1:
            qs = self.model.objects.all()
        elif user.type == 6:
            qs = self.model.objects.filter(client__city__in=user.superviser.city_id_list())
        elif user.type == 2:
            qs = self.model.objects.filter(client__city__moderator=user)
        elif user.type == 5:
            if user.is_leader_manager():
                qs = self.model.objects.filter(client__city__moderator=user.manager.moderator)
            else:
                qs = self.model.objects.filter(client__manager=user.manager)
        else:
            qs = self.model.objects.none()
        return qs


class ClientJournal(models.Model):
    client = models.ForeignKey(on_delete=models.CASCADE, to=Client, verbose_name=u'клиент')
    clientorder = models.ManyToManyField(to=ClientOrder, verbose_name=u'заказ клиента')
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=u'Цена за стенд, руб')
    add_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=u'Наценка, %', blank=True, null=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=u'Скидка, %', blank=True, null=True)
    created = models.DateField(auto_now_add=True, verbose_name=u'Дата создания')
    has_payment = models.BooleanField(default=False, verbose_name=u'Есть поступления')
    full_payment = models.BooleanField(default=False, verbose_name=u'Оплачено')
    total_stand_count = models.IntegerField(blank=True, null=True, default=0)
    full_cost = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, default=0)
    total_payment = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, default=0)

    objects = ClientJournalModelManager()

    class Meta:
        verbose_name = u'Покупка'
        verbose_name_plural = u'Покупки'
        app_label = 'client'
        ordering = ('-id',)

    def __unicode__(self):
        return u'Покупка на дату %s' % self.created

    def __str__(self):
        return self.__unicode__()

    def current_payment(self):
        """
        Показывает текущую сумму поступлений по покупке
        """
        count = 0
        for payment in self.clientjournalpayment_set.all():
            count += payment.sum
        return round(count, 2)

    def stand_count(self):
        """
        Показывает количество стендов в покупке
        """
        stand_count = 0
        for clientorder in self.clientorder.all():
            stand_count += clientorder.stand_count()
        return stand_count

    def total_cost(self):
        """
        Показывает общую стоимость покупки
        """
        cost = self.cost
        if self.add_cost:
            add_cost = self.add_cost
        else:
            add_cost = 0
        if self.discount:
            discount = self.discount
        else:
            discount = 0
        sum = ((float(cost) * (1 + float(add_cost) * 0.01)) * (1 - float(discount) * 0.01)) * self.stand_count()
        return round(sum, 2)

    def price_without_stands(self):
        """
        Полная стоимость за 1 стенд
        """
        cost = self.cost
        if self.add_cost:
            add_cost = self.add_cost
        else:
            add_cost = 0
        if self.discount:
            discount = self.discount
        else:
            discount = 0
        sum = ((cost * (1 + add_cost * 0.01)) * (1 - discount * 0.01))
        return round(sum, 2)

    # def save(self, force_insert=False, force_update=False, using=None,
    #          update_fields=None):
    #     super(ClientJournal, self).save()
    #     self.total_stand_count = self.stand_count()
    #     self.full_cost = self.total_cost()
    #     self.save()


class ClientJournalPaymentModelManager(models.Manager):
    def get_qs(self, user):
        if user.type == 1:
            qs = self.model.objects.all()
        elif user.type == 6:
            qs = self.model.objects.filter(client__city__in=user.superviser.city_id_list())
        elif user.type == 2:
            qs = self.model.objects.filter(client__manager__moderator=user)
        elif user.type == 5:
            if user.is_leader_manager():
                qs = self.model.objects.filter(client__city__moderator=user.manager.moderator)
            else:
                qs = self.model.objects.filter(client__manager=user.manager)
        else:
            qs = self.model.objects.none()
        return qs


class ClientJournalPayment(models.Model):
    client = models.ForeignKey(on_delete=models.CASCADE, to=Client, verbose_name=u'Клиент')
    clientjournal = models.ForeignKey(on_delete=models.CASCADE, to=ClientJournal, verbose_name=u'Покупка')
    sum = models.DecimalField(max_digits=11, decimal_places=2, verbose_name=u'Сумма')
    created = models.DateField(auto_now_add=True, verbose_name=u'Дата создания')

    objects = ClientJournalModelManager()

    class Meta:
        verbose_name = u'Поступление'
        verbose_name_plural = u'Поступления'
        app_label = 'client'
        ordering = ['-created']

    def __unicode__(self):
        return u'Поступление на сумму %s руб. Дата: %s' % (self.sum, self.created)

    def __str__(self):
        return self.__unicode__()

    def save(self, *args, **kwargs):
        super(ClientJournalPayment, self).save()
        clientjournal = self.clientjournal
        clientjournal.has_payment = True
        if clientjournal.current_payment() >= clientjournal.total_cost():
            clientjournal.full_payment = True
        else:
            clientjournal.full_payment = False
        clientjournal.save()


@receiver(post_save, sender=ClientJournalPayment)
def increment_payment_for_clientjournal(sender, created, **kwargs):
    """
    Увеличение суммы поступлений в журнале продажи
    """
    instance = kwargs['instance']
    clientjournal = instance.clientjournal
    if created:
        if clientjournal.total_payment:
            clientjournal.total_payment = float(clientjournal.total_payment) + float(instance.sum)
        else:
            clientjournal.total_payment = instance.sum
        clientjournal.save()


@receiver(post_delete, sender=ClientJournalPayment)
def decrement_payment_for_clientjournal(sender, **kwargs):
    """
    Уменшение суммы поступлений в журнале продажи
    """
    instance = kwargs['instance']
    clientjournal = instance.clientjournal
    clientjournal.total_payment -= instance.sum
    clientjournal.save()


class ClientMaket(models.Model):
    client = models.ForeignKey(on_delete=models.CASCADE, to=Client, verbose_name=u'Клиент')
    name = models.CharField(max_length=256, verbose_name=u'Название')
    file = models.FileField(verbose_name=u'Файл макета', upload_to=upload_to)
    date = models.DateField(verbose_name=u'Дата размещения макета')

    class Meta:
        verbose_name = u'Макет'
        verbose_name_plural = u'Макеты'
        app_label = 'client'
        ordering = ['-date']

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()


class ClientSurfaceBind(models.Model):
    client = models.ForeignKey(Client, verbose_name='Клиент', on_delete=models.CASCADE)
    surface = models.ForeignKey(Surface, verbose_name='Поверхность (адрес)', on_delete=models.CASCADE)

    class Meta:
        app_label = 'client'
        verbose_name = 'Зона покрытия (адреса присутствия услуг)'
        verbose_name_plural = 'Зоны покрытия (адреса присутствия услуг)'

    def __str__(self):
        return f'{self.client}, {self.surface}'
