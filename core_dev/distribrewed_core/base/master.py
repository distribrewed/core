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

    def _on_ready(self):
        super(BaseMaster, self)._on_ready()

    def _call_worker_method(self, worker_id=None, all_workers=False, method='NONAME', args=[]):
        tasks.worker.call_method_by_name.apply_async(
            worker_id=worker_id,
            all_workers=all_workers,
            args=[method] + args
        )
        if all_workers:
            CALLS_TO_WORKERS.labels('all').inc()
        if worker_id:
            CALLS_TO_WORKERS.labels(worker_id).inc()

    def register_worker(self, worker_id, worker_info, worker_methods, reload_queues=False):
        log.info("Registering '{0}' ; Info : {1} ; Methods : {2}".format(
            worker_id,
            json.dumps(worker_info, sort_keys=True),
            json.dumps(worker_methods, sort_keys=True)
        ))
        if reload_queues:
            self.reload_queues()

    def reload_queues(self):
        kombu.pools.reset()  # TODO: Maybe a little drastic / find a better way

    def de_register_worker(self, worker_id, worker_info):
        log.info("De-registering '{0}': {1}".format(worker_id, json.dumps(worker_info, sort_keys=True)))

    def ping_worker(self, worker_id):
        log.info("Sending ping to '{0}'".format(worker_id))
        self._call_worker_method(worker_id=worker_id, method='handle_ping')

    def handle_ping(self, worker_id):
        log.info("Received ping from '{0}'".format(worker_id))
        self._call_worker_method(worker_id=worker_id, method='handle_pong')

    def handle_pong(self, worker_id):
        log.info("Received pong from '{0}'".format(worker_id))

    def command_all_workers_to_ping_master(self):
        log.info("Commanding all workers to ping master")
        self._call_worker_method(all_workers=True, method='ping_master')

    def command_all_workers_to_register(self):
        log.info("Commanding all workers to re-register")
        self._call_worker_method(all_workers=True, method='register')

    def command_all_workers_to_de_register(self):
        log.info("Commanding all workers to re-register")
        self._call_worker_method(all_workers=True, method='de_register')

    def request_worker_method_list(self, worker_id):
        log.info("Requesting method list from worker {0}".format(worker_id))
        self._call_worker_method(worker_id=worker_id, method='send_method_list')

    def receive_worker_method_list(self, worker_id, method_list):
        log.info("{0} methods: {1}".format(worker_id, method_list))

    def request_worker_method_parameter_list(self, worker_id, method_name):
        log.info("Requesting method parameter list of '{0}' from worker {1}".format(method_name, worker_id))
        self._call_worker_method(worker_id=worker_id, method='send_method_parameter_list', args=[method_name])

    def receive_worker_method_parameter_list(self, worker_id, method_name, parameter_names):
        log.info("{0} method {1} parameters: {2}".format(worker_id, method_name, parameter_names))

    def request_worker_start(self, worker_id, schedule):
        log.info("Requesting worker start {0}".format(worker_id))
        self.call_worker_method(worker_id=worker_id, method='start_worker', args=[schedule])

    def request_worker_stop(self, worker_id):
        log.info("Requesting worker stop {0}".format(worker_id))
        self.call_worker_method(worker_id=worker_id, method='stop_worker')

    def request_worker_pause(self, worker_id):
        log.info("Requesting worker pause {0}".format(worker_id))
        self.call_worker_method(worker_id=worker_id, method='pause_worker')

    def request_worker_resume(self, worker_id):
        log.info("Requesting worker pause {0}".format(worker_id))
        self.call_worker_method(worker_id=worker_id, method='resume_worker')