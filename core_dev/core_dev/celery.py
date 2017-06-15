from __future__ import absolute_import, unicode_literals

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core_dev.settings.settings")

from distribrewed_core.celery import *
# noinspection PyUnresolvedReferences
import distribrewed_core.tasks

queue.config_from_object('django.conf:settings', namespace='CELERY')
