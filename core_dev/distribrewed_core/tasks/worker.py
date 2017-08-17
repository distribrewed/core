from __future__ import absolute_import, unicode_literals

from celery import shared_task

from distribrewed_core.tasks import worker_plugin


@shared_task
def call_method_by_name(method, *args):
    getattr(worker_plugin, method)(*args)
