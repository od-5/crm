# coding=utf-8
import datetime
from django.conf import settings
import datetime
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
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
        release_date = datetime.datetime.utcnow().replace(tzinfo=utc) - datetime.timedelta(days=365)
        if self.clientordersurface_set.all():
            for c_surface in self.clientordersurface_set.all():
                surface = Surface.objects.get(pk=c_surface.surface.id)
                surface.free = True
                surface.release_date = release_date.date()
                surface.save()
        super(ClientOrder, self).delete()

    def stand_count(self):
        if self.clientordersurface_set.select_related().all():
            total = 0
            for i in self.clientordersurface_set.select_related().all():
                total += i.porch_count()
            return total
        else:
            return 0

    client = models.ForeignKey(to=Client, verbose_name=u'Клиент')
    date_start = models.DateField(verbose_name=u'Дата начала размещения')
    date_end = models.DateField(verbose_name=u'Дата окончания размещения')
    is_closed = models.BooleanField(verbose_name=u'Заказ закрыт', default=False)


class ClientOrderSurface(models.Model):
    class Meta:
        verbose_name = u'Пункт заказа'
        verbose_name_plural = u'Пункты заказа'
        app_label = 'client'

    def __unicode__(self):
        return u'%s %s ' % (self.surface.street.name, self.surface.house_number)

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

    clientorder = models.ForeignKey(to=ClientOrder, verbose_name=u'Заказ')
    surface = models.ForeignKey(to=Surface, verbose_name=u'Рекламная поверхность')


class ClientJournal(models.Model):
    class Meta:
        verbose_name = u'Покупка'
        verbose_name_plural = u'Покупки'
        app_label = 'client'

    def __unicode__(self):
        return u'Покупка на дату %s' % self.created

    def current_payment(self):
        """
        Показывает текущую сумму поступлений по покупке
        """
        count = 0
        for payment in self.clientjournalpayment_set.select_related().all():
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
        sum = ((float(cost)*(1+float(add_cost)*0.01))*(1-float(discount)*0.01)) * self.stand_count()
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
        sum = ((cost*(1+add_cost*0.01))*(1-discount*0.01))
        return round(sum, 2)

    # def save(self, force_insert=False, force_update=False, using=None,
    #          update_fields=None):
    #     super(ClientJournal, self).save()
    #     self.total_stand_count = self.stand_count()
    #     self.full_cost = self.total_cost()
    #     self.save()

    client = models.ForeignKey(to=Client, verbose_name=u'клиент')
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


class ClientJournalPayment(models.Model):
    class Meta:
        verbose_name = u'Поступление'
        verbose_name_plural = u'Поступления'
        app_label = 'client'
        ordering = ['-created']

    def __unicode__(self):
        return u'Поступление на сумму %s руб. Дата: %s' % (self.sum, self.created)

    def save(self, *args, **kwargs):
        super(ClientJournalPayment, self).save()
        clientjournal = self.clientjournal
        clientjournal.has_payment = True
        if clientjournal.current_payment() >= clientjournal.total_cost():
            clientjournal.full_payment = True
        else:
            clientjournal.full_payment = False
        clientjournal.save()

    client = models.ForeignKey(to=Client, verbose_name=u'Клиент')
    clientjournal = models.ForeignKey(to=ClientJournal, verbose_name=u'Покупка')
    sum = models.DecimalField(max_digits=11, decimal_places=2, verbose_name=u'Сумма')
    created = models.DateField(auto_now_add=True, verbose_name=u'Дата создания')
#     todo: добавить post_save сигнал для перерасчёта полной суммы поступлений по покупке


@receiver(post_save, sender=ClientJournalPayment)
def increment_payment_for_clientjournal(sender, created, **kwargs):
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
    instance = kwargs['instance']
    clientjournal = instance.clientjournal
    clientjournal.total_payment -= instance.sum
    clientjournal.save()


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
