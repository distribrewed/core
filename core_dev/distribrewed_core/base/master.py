import logging

from distribrewed_core import tasks

log = logging.getLogger(__name__)


# noinspection PyMethodMayBeStatic
class BaseMaster:
    def __init__(self):
        pass

    def call_worker_method(self, worker_id=None, all_workers=False, method='NONAME', args=[]):
        tasks.worker.call_method_by_name.apply_async(
            worker_id=worker_id,
            all_workers=all_workers,
            args=[method] + args
        )

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
