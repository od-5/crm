# coding=utf-8
import os
import uuid
from django.conf import settings
from django.db import models
from imagekit.models import ImageSpecField
from pilkit.processors import SmartResize

from core.base_model import Common

__author__ = 'alexy'
