from __future__ import absolute_import, unicode_literals

from celery import shared_task

from distribrewed_core.tasks import worker_plugin


# Ping / Pong

@shared_task
def ping_master():
    worker_plugin.ping_master()


@shared_task
def handle_ping():
    worker_plugin.handle_ping()


@shared_task
def handle_pong():
    worker_plugin.handle_pong()


# Methods

@shared_task
def send_method_list():
    worker_plugin.send_method_list()


@shared_task
def call_method_by_name(method):
    getattr(worker_plugin, method)()
