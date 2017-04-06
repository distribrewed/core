from __future__ import absolute_import, unicode_literals

import logging

from celery import shared_task

from distribrewed.core.tasks import master_plugin

log = logging.getLogger(__name__)


# Ping / Pong

@shared_task
def ping_worker(worker_id):
    master_plugin.ping_worker(worker_id)


@shared_task
def handle_ping(worker_id):
    master_plugin.handle_ping(worker_id)


@shared_task
def handle_pong(worker_id):
    master_plugin.handle_pong(worker_id)


@shared_task
def command_all_workers_to_ping_master():
    master_plugin.command_all_workers_to_ping_master()


# Methods

@shared_task
def request_worker_method_list(worker_id):
    master_plugin.request_worker_method_list(worker_id)


@shared_task
def receive_worker_method_list(worker_id, method_list):
    master_plugin.receive_worker_method_list(worker_id, method_list)


@shared_task
def call_worker_method_by_name(worker_id, method):
    master_plugin.call_worker_method_by_name(worker_id, method)
