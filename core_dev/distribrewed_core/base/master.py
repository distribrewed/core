import datetime
import json
import logging

import kombu
from prometheus_client import Counter

from distribrewed_core import tasks
from distribrewed_core.base.celery import CeleryWorker

log = logging.getLogger(__name__)


# noinspection PyMethodMayBeStatic
class BaseMaster(CeleryWorker):
    def __init__(self):
        try:
            BaseMaster.CALLS_TO_WORKERS = Counter('CALLS_TO_WORKERS', 'Number of calls to workers', ['worker'])
        except ValueError:
            pass  # It is already defined

    def _on_ready(self):
        super(BaseMaster, self)._on_ready()

    def _call_worker_method(self, worker_id=None, all_workers=False, method='NONAME', args=[]):
        assert worker_id or all_workers, 'You must give a worker_id or send to all_workers'
        assert bool(worker_id) != bool(all_workers), 'You cannot both send to worker_id and all_workers'
        log.debug('Calling worker method {}({}) worker_id: {}, all_workers: {}'.format(
            method,
            ', '.join([str(a) for a in args]),
            worker_id,
            all_workers
        ))
        tasks.worker.call_method_by_name.apply_async(
            worker_id=worker_id,
            all_workers=all_workers,
            args=[method] + args
        )
        if all_workers:
            self.CALLS_TO_WORKERS.labels('all').inc()
        if worker_id:
            self.CALLS_TO_WORKERS.labels(worker_id).inc()

    # Registration methods

    def reload_queues(self):
        kombu.pools.reset()  # TODO: Maybe a little drastic / find a better way

    def _register_worker(self, worker_id, worker_info, worker_methods, reload_queues=False):
        log.info("Registering '{0}' ; Info : {1} ; Methods : {2}".format(
            worker_id,
            json.dumps(worker_info, sort_keys=True),
            json.dumps(worker_methods, sort_keys=True)
        ))
        if reload_queues:
            self.reload_queues()

    def _de_register_worker(self, worker_id, worker_info):
        log.info("De-registering '{0}': {1}".format(worker_id, json.dumps(worker_info, sort_keys=True)))

    def command_all_workers_to_register(self):
        log.info("Commanding all workers to re-register")
        self._call_worker_method(all_workers=True, method='register')

    def command_all_workers_to_de_register(self):
        log.info("Commanding all workers to re-register")
        self._call_worker_method(all_workers=True, method='de_register')

    # Ping methods

    def ping_worker(self, worker_id=None, all_workers=None):
        log.info("Sending ping to '{0}'".format(worker_id))
        self._call_worker_method(worker_id=worker_id, all_workers=all_workers, method='_handle_ping')

    def _handle_ping(self, worker_id):
        log.info("Received ping from '{0}'".format(worker_id))
        self._call_worker_method(worker_id=worker_id, method='_handle_pong')

    def _handle_pong(self, worker_id):
        log.info("Received pong from '{0}'".format(worker_id))

    def command_all_workers_to_ping_master(self):
        log.info("Commanding all workers to ping master")
        self._call_worker_method(all_workers=True, method='ping_master')

    # Time sync

    def send_time_sync_to_worker(self, worker_id=None, all_workers=None):
        log.info("Sending time sync to {}".format(worker_id if worker_id else 'all workers'))
        self._call_worker_method(
            worker_id=worker_id,
            all_workers=all_workers,
            method='_handle_time_sync_request',
            args=[datetime.datetime.now()]
        )

    def _handle_time_sync_request(self, worker_id):
        log.info("Received time sync request from {0}".format(worker_id))
        self.send_time_sync_to_worker(worker_id)

    def command_all_workers_to_time_sync(self):
        self._call_worker_method(all_workers=True, method='time_sync')


# Schedule master
class ScheduleMaster(BaseMaster):
    def __init__(self):
        super(ScheduleMaster, self).__init__()

    def request_worker_start(self, worker_id, schedule):
        log.info("Requesting worker start {0}".format(worker_id))
        self._call_worker_method(worker_id=worker_id, method='start_worker', args=[schedule])

    def request_worker_stop(self, worker_id):
        log.info("Requesting worker stop {0}".format(worker_id))
        self._call_worker_method(worker_id=worker_id, method='stop_worker')

    def request_worker_pause(self, worker_id):
        log.info("Requesting worker pause {0}".format(worker_id))
        self._call_worker_method(worker_id=worker_id, method='pause_worker')

    def request_worker_resume(self, worker_id):
        log.info("Requesting worker pause {0}".format(worker_id))
        self._call_worker_method(worker_id=worker_id, method='resume_worker')

    def request_worker_status(self, worker_id=None, all_workers=None):
        self._call_worker_method(worker_id=worker_id, all_workers=all_workers, method='send_status_to_master')

    def _handle_status_from_worker(self, worker_id, is_running, is_paused):
        log.info("Worker {0} status: is_running = {1}, is_paused = {2}".format(worker_id, is_running, is_paused))
