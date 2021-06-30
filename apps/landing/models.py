# coding=utf-8
from PIL import Image
from django.conf import settings
from django.db import models
from imagekit.models import ImageSpecField
from pilkit.processors import SmartResize
from apps.city.models import City
from core.files import upload_to

__author__ = 'alexy'


class Setup(models.Model):
    class Meta:
        verbose_name = u'Настройки сайта'
        verbose_name_plural = u'Настройки сайта'
        app_label = 'landing'
        ordering = ('id', )

    def __unicode__(self):
        if self.city:
            return u'Настройки сайта для города %s' % self.city.name
        else:
            return u'Настройки основного сайта'

    def save(self, *args, **kwargs):
        super(Setup, self).save()
        if self.logotype:
            image = Image.open(self.logotype)
            (width, height) = image.size
            size = (350, 350)
            "Max width and height 350"
            if width > 350:
                image.thumbnail(size, Image.ANTIALIAS)
                image.save(self.logotype.path, "PNG")

    city = models.OneToOneField(on_delete=models.CASCADE, to=City, verbose_name=u'Город', null=True, blank=True)
    logotype = models.ImageField(verbose_name=u'Логотип', blank=True, null=True, upload_to=upload_to)
    meta_title = models.TextField(verbose_name=u'Заголовок сайта', blank=True, null=True)
    meta_keys = models.TextField(verbose_name=u'Ключевые слова', blank=True, null=True)
    meta_desc = models.TextField(verbose_name=u'Мета описание', blank=True, null=True)
    email = models.EmailField(verbose_name=u'e-mail для приёма заявок', blank=True)
    phone = models.CharField(verbose_name=u'Контактный телефон', blank=True, null=True, max_length=20)
    video_find = models.CharField(verbose_name=u'Видео: как найти наш офис', blank=True, null=True, max_length=256)
    video = models.TextField(verbose_name=u'HTML-код видео: что получать наши клиенты', blank=True, null=True)
    top_js = models.TextField(verbose_name=u'Скрипты в <HEAD>..</HEAD>', blank=True)
    bottom_js = models.TextField(verbose_name=u'Скрипты перед закрывающим </BODY>', blank=True)
    robots_txt = models.TextField(verbose_name=u'robots.txt', blank=True, null=True)


class BlockEffective(models.Model):
    class Meta:
        verbose_name = u'Почему реклама настолько эффективна'
        verbose_name_plural = u'Почему реклама настолько эффективна'
        app_label = 'landing'
        ordering = ('city', )

    def __unicode__(self):
        return u'Почему реклама на подъездах настолько эффективна'

    city = models.ForeignKey(on_delete=models.CASCADE, to=City, verbose_name=u'Город', null=True, blank=True)
    image = models.ImageField(verbose_name=u'иконка', upload_to=upload_to)
    text = models.TextField(verbose_name=u'Текст')


class BlockExample(models.Model):
    class Meta:
        verbose_name = u'Прмеры размещений'
        verbose_name_plural = u'Прмеры размещений'
        app_label = 'landing'
        ordering = ('city', )

    def __unicode__(self):
        return self.name

    city = models.ForeignKey(on_delete=models.CASCADE, to=City, verbose_name=u'Город', null=True, blank=True)
    name = models.CharField(verbose_name=u'Название фотографии(адрес)', max_length=256)
    image = models.ImageField(verbose_name=u'Фотография', upload_to=upload_to)
    image_resize = ImageSpecField(
        [SmartResize(*settings.EXAMPLE_THUMB_SIZE)], source='image', format='JPEG', options={'quality': 94}
    )


class BlockReview(models.Model):
    class Meta:
        verbose_name = u'Отзыв'
        verbose_name_plural = u'Отзывы'
        app_label = 'landing'
        ordering = ('city', )

    def __unicode__(self):
        return self.name

    city = models.ForeignKey(on_delete=models.CASCADE, to=City, verbose_name=u'Город', null=True, blank=True)
    name = models.CharField(verbose_name=u'ФИО', max_length=256)
    image = models.ImageField(verbose_name=u'Фотография', upload_to=upload_to)
    image_resize = ImageSpecField(
        [SmartResize(*settings.REVIEW_THUMB_SIZE)], source='image', format='JPEG', options={'quality': 94}
    )
    link = models.CharField(verbose_name=u'ссылка', max_length=256, blank=True, null=True)
    description = models.TextField(verbose_name=u'Описание(компания, должность)')
    text = models.TextField(verbose_name=u'Текст комментария')

