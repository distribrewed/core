from __future__ import absolute_import, unicode_literals

import logging

from celery import shared_task

from distribrewed_core.tasks import master_plugin

log = logging.getLogger(__name__)


@shared_task
def call_method_by_name(method, *args):
    getattr(master_plugin, method)(*args)
