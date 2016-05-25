# coding=utf-8
from os import path as op
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

    # if not op.exists(root_dir):
    #     makedirs(root_dir)
    # print root_dir
    name = slugify(instance.__unicode__())
    filename = "%s%s" % (name, ext or '.jpg')
    basedir = op.join(instance._meta.model_name, instance.porch.surface.city.slug)
    if prefix:
        basedir = op.join(basedir, prefix)
    return op.join(basedir, filename)
