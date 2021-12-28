from os import path as op
import random
import string
import uuid
from pytils.translit import slugify

__author__ = 'aser'


class UploadTo(object):
    def __init__(self, prefix=None):
        self.prefix = prefix

    def __call__(self, *args, **kwargs):
        return self.upload_to(*args, prefix=self.prefix)

    @staticmethod
    def upload_to(instance, filename, prefix=None):
        """
        Auto generate name for File and Image fields.
        :param instance: Instance of Model
        :param filename: Name of uploaded file
        :param prefix: Add to path
        :return:
        """
        name, ext = op.splitext(filename)
        filename = "%s%s" % (uuid.uuid4(), ext or '.jpg')
        basedir = op.join(instance._meta.app_label, instance._meta.model_name)
        if prefix:
            basedir = op.join(basedir, prefix)
        return op.join(basedir, filename[:2], filename[2:4], filename)


def upload_to(instance, filename, prefix=None):
        """
        Auto generate name for File and Image fields.
        :param instance: Instance of Model
        :param filename: Name of uploaded file
        :param prefix: Add to path
        :return:
        """
        name, ext = op.splitext(filename)
        filename = "%s%s" % (uuid.uuid4(), ext or '.jpg')
        basedir = op.join(instance._meta.app_label, instance._meta.model_name)
        if prefix:
            basedir = op.join(basedir, prefix)
        return op.join(basedir, filename[:2], filename[2:4], filename)


def surfacephoto_upload(instance, filename, prefix=None):
    """
    Auto generate name for File and Image fields.
    :param instance: Instance of Model
    :param filename: Name of uploaded file
    :param prefix: Add to path
    :return:
    """
    ext = op.splitext(filename)[-1]
    name = slugify(instance.__unicode__())
    filename = f'{name}_{rnd_string()}{ext}'
    basedir = op.join(instance._meta.model_name, instance.porch.surface.city.slug)
    if prefix:
        basedir = op.join(basedir, prefix)
    return op.join(basedir, filename)


def rnd_string(n=10):
    return ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=10))
