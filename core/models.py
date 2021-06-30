# coding=utf-8
import os
from random import randint
import uuid
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
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
        user.type = 1
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
    work_basis = models.CharField(max_length=256, blank=True, null=True, verbose_name=u'Действует на основании')

    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin site.'))

    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    # def save(self, force_insert=False, force_update=False, using=None,
    #          update_fields=None):
    #     if self.type == 1 and not self.is_superuser:
    #         self.is_superuser = True
    #     else:
    #         self.is_superuser = False
    #     super(User, self).save()

    @classmethod
    def get_moderator_qs(cls, user):
        if user.type == 1:
            qs = cls.objects.filter(type=2)
        elif user.type == 6:
            qs = cls.objects.filter(pk__in=user.superviser.moderator_id_list())
        else:
            qs = cls.objects.none()
        return qs

    def is_leader_manager(self):
        if self.type == 1 or self.type == 2 or self.type == 6:
            return True
        if self.type == 5:
            if self.manager.leader:
                return True
        return False

    def get_absolute_url(self):
        if self.type == 1:
            return reverse('administrator:update', args=(self.pk,))
        if self.type == 2:
            return reverse('moderator:change', args=(self.pk,))
        else:
            return reverse('cabinet:cabinet')

    def get_change_url(self):
        return reverse('cabinet:user-change', args=(self.pk,))

    def get_full_name(self):
        if self.last_name:
            return u'%s %s %s' % (self.last_name, self.first_name or '', self.patronymic or '')
        return self.email

    def get_short_name(self):
        return u'%s' % self.first_name

    def __unicode__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
