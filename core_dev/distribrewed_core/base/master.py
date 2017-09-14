import json
import logging

import kombu
from prometheus_client import Counter

from distribrewed_core import tasks
from distribrewed_core.base.celery import CeleryWorker

log = logging.getLogger(__name__)

CALLS_TO_WORKERS = Counter('CALLS_TO_WORKERS', 'Number of calls to workers', ['worker'])


# noinspection PyMethodMayBeStatic
class BaseMaster(CeleryWorker):
    def __init__(self):
        pass

    def on_ready(self):
        super(BaseMaster, self).on_ready()

    def call_worker_method(self, worker_id=None, all_workers=False, method='NONAME', args=[]):
        tasks.worker.call_method_by_name.apply_async(
            worker_id=worker_id,
            all_workers=all_workers,
            args=[method] + args
        )
        if all_workers:
            CALLS_TO_WORKERS.labels('all').inc()
        if worker_id:
            CALLS_TO_WORKERS.labels(worker_id).inc()

    def register_worker(self, worker_id, worker_info):
        log.info("Registering '{0}': {1}".format(worker_id, json.dumps(worker_info, sort_keys=True)))
        kombu.pools.reset()  # TODO: Maybe a little drastic

    def de_register_worker(self, worker_id, worker_info):
        log.info("De-registering '{0}': {1}".format(worker_id, json.dumps(worker_info, sort_keys=True)))

    def ping_worker(self, worker_id):
        log.info("Sending ping to '{0}'".format(worker_id))
        self.call_worker_method(worker_id=worker_id, method='handle_ping')

    def handle_ping(self, worker_id):
        log.info("Received ping from '{0}'".format(worker_id))
        self.call_worker_method(worker_id=worker_id, method='handle_pong')

    def handle_pong(self, worker_id):
        log.info("Received pong from '{0}'".format(worker_id))

    def command_all_workers_to_ping_master(self):
        log.info("Commanding all workers to ping master")
        self.call_worker_method(all_workers=True, method='ping_master')

    def request_worker_method_list(self, worker_id):
        log.info("Requesting method list from worker {0}".format(worker_id))
        self.call_worker_method(worker_id=worker_id, method='send_method_list')

    def receive_worker_method_list(self, worker_id, method_list):
        log.info("{0} methods: {1}".format(worker_id, method_list))

    def request_worker_method_parameter_list(self, worker_id, method_name):
        log.info("Requesting method parameter list of '{0}' from worker {1}".format(method_name, worker_id))
        self.call_worker_method(worker_id=worker_id, method='send_method_parameter_list', args=[method_name])

    def receive_worker_method_parameter_list(self, worker_id, method_name, parameter_names):
        log.info("{0} method {1} parameters: {2}".format(worker_id, method_name, parameter_names))
