from __future__ import absolute_import, unicode_literals

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core_dev.settings.settings")

from distribrewed.core.celery import *
# noinspection PyUnresolvedReferences
import distribrewed.core.tasks

queue.config_from_object('django.conf:settings', namespace='CELERY')
