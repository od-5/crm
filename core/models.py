# coding=utf-8
import os
from random import randint
import uuid
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from imagekit.models import ImageSpecField
from pilkit.processors import SmartResize
from core.files import upload_to

__author__ = 'alexy'


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')

        if not password:
            password = User.objects.make_random_password()

        kwargs.update({'email': self.normalize_email(email)})
        user = self.model(**kwargs)
        user.set_password(password)
        user.original_password = password
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, first_name=None, last_name=None, patronymic=None):
        user = self.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            patronymic=patronymic,
        )

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def normalize_email(self, email):
        email = super(MyUserManager, self).normalize_email(email)
        return email.lower()


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = u'Пользователь'
        verbose_name_plural = u'Пользователи'
        ordering = ['-date_joined']
        app_label = 'core'

    USER_TYPE_CHOICE = (
        (1, u'Администратор'),
        (2, u'Модератор'),
        (3, u'Клиент'),
        (4, u'Монтажник'),
        (5, u'Менеджер'),
    )

    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True, null=True, default=u'')
    last_name = models.CharField(_('last name'), max_length=30, blank=True, null=True, default=u'')
    patronymic = models.CharField(u'Отчество', max_length=50, blank=True, null=True, default=u'')
    phone = models.CharField(max_length=250, verbose_name=u'Телефон', null=True, blank=True, default=u'')
    type = models.PositiveSmallIntegerField(verbose_name=u'Уровень доступа', default=3, choices=USER_TYPE_CHOICE)
    company = models.CharField(max_length=100, blank=True, null=True, verbose_name=u'Название организации')
    leader = models.CharField(max_length=100, blank=True, null=True, verbose_name=u'Руководитель')
    leader_function = models.CharField(max_length=100, blank=True, null=True, verbose_name=u'Должность руководителя')
    work_basis = models.CharField(max_length=256, blank=True, null=True, verbose_name=u'Договора франшизы')

    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin site.'))

    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.type == 1 and not self.is_superuser:
            self.is_superuser = True
        else:
            self.is_superuser = False
        super(User, self).save()

    def get_absolute_url(self):
        if self.type == 1:
            return reverse('administrator:change', args=(self.pk, ))
        if self.type == 2:
            return reverse('moderator:change', args=(self.pk, ))
        else:
            return reverse('cabinet:cabinet')

    def get_change_url(self):
        return reverse('cabinet:user-change', args=(self.pk, ))

    def get_full_name(self):
        return u'%s %s %s' % (self.last_name, self.first_name or '', self.patronymic or '')

    def get_short_name(self):
        return u'%s' % self.first_name

    def __unicode__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class Setup(models.Model):
    class Meta:
        verbose_name = u'Настройки сайта'
        verbose_name_plural = u'Настройки сайта'
        app_label = 'core'

    def __unicode__(self):
        return u'Настройки сайта'

    meta_title = models.TextField(verbose_name=u'Заголовок сайта', blank=True, null=True)
    meta_keys = models.TextField(verbose_name=u'Ключевые слова', blank=True, null=True)
    meta_desc = models.TextField(verbose_name=u'Мета описание', blank=True, null=True)
    email = models.EmailField(verbose_name=u'e-mail для приёма заявок', blank=True)
    phone = models.CharField(verbose_name=u'Контактный телефон', blank=True, null=True, max_length=20)
    video = models.TextField(verbose_name=u'HTML-код видео', blank=True, null=True)
    top_js = models.TextField(verbose_name=u'Скрипты в <HEAD>..</HEAD>', blank=True)
    bottom_js = models.TextField(verbose_name=u'Скрипты перед закрывающим </BODY>', blank=True)
    robots_txt = models.TextField(verbose_name=u'robots.txt', blank=True, null=True)


class BlockEffective(models.Model):
    class Meta:
        verbose_name = u'Почему реклама настолько эффективна'
        verbose_name_plural = u'Почему реклама настолько эффективна'
        app_label = 'core'

    def __unicode__(self):
        return u'Почему реклама на подъездах настолько эффективна'

    image = models.ImageField(verbose_name=u'иконка', upload_to=upload_to)
    text = models.TextField(verbose_name=u'Текст')


class BlockExample(models.Model):
    class Meta:
        verbose_name = u'Прмеры размещений'
        verbose_name_plural = u'Прмеры размещений'
        app_label = 'core'

    def __unicode__(self):
        return self.name

    name = models.CharField(verbose_name=u'Название фотографии(адрес)', max_length=256)
    image = models.ImageField(verbose_name=u'Фотография', upload_to=upload_to)
    image_resize = ImageSpecField(
        [SmartResize(*settings.EXAMPLE_THUMB_SIZE)], source='image', format='JPEG', options={'quality': 94}
    )


class BlockReview(models.Model):
    class Meta:
        verbose_name = u'Отзыв'
        verbose_name_plural = u'Отзывы'
        app_label = 'core'

    def __unicode__(self):
        return self.name

    name = models.CharField(verbose_name=u'ФИО', max_length=256)
    image = models.ImageField(verbose_name=u'Фотография', upload_to=upload_to)
    image_resize = ImageSpecField(
        [SmartResize(*settings.REVIEW_THUMB_SIZE)], source='image', format='JPEG', options={'quality': 94}
    )
    link = models.CharField(verbose_name=u'ссылка', max_length=256, blank=True, null=True)
    description = models.TextField(verbose_name=u'Описание(компания, должность)')
    text = models.TextField(verbose_name=u'Текст комментария')
