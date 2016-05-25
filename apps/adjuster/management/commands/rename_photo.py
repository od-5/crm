# coding=utf-8
from os import path as op
from os import makedirs
from django.conf import settings
from PIL import Image
from django.core.management.base import BaseCommand, CommandError
from pytils.translit import slugify
from apps.adjuster.models import SurfacePhoto

__author__ = 'alexy'


class Command(BaseCommand):

    def handle(self, *args, **options):
        qs = SurfacePhoto.objects.all()
        for i in qs:
            media_root = settings.MEDIA_ROOT
            subdir = op.join(i._meta.model_name, i.porch.surface.city.slug)
            root_dir = op.join(media_root, subdir)
            if not op.exists(root_dir):
                makedirs(root_dir)
            ext = op.splitext(i.image.path)[-1]
            if
            name = slugify(i.__unicode__())
            filename = "id%s_%s%s" % (i.id, name, ext or '.jpg')
            short_path = op.join(subdir, filename)
            full_path = op.join(root_dir, filename)
            try:
                print 'open image'
                image = Image.open(i.image.path)
                image.save(full_path, "PNG")
                print 'image save complete'
            except:
                print 'image save fail'
            try:
                print 'set new path for instance'
                i.image = short_path
                i.save()
                print 'instance save ok'
            except:
                print 'instance save fail'