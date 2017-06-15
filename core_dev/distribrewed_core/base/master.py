import logging

from distribrewed_core import tasks

log = logging.getLogger(__name__)


class BaseMaster:
    def __init__(self):
        pass

    def ping_worker(self, worker_id):
        log.info("Sending ping to '{0}'".format(worker_id))
        tasks.worker.handle_ping.apply_async(worker_id=worker_id)

    def handle_ping(self, worker_id):
        log.info("Received ping from '{0}'".format(worker_id))
        tasks.worker.handle_pong.apply_async(worker_id=worker_id)

    def handle_pong(self, worker_id):
        log.info("Received pong from '{0}'".format(worker_id))

    def command_all_workers_to_ping_master(self):
        log.info("Commanding all workers to ping master")
        tasks.worker.ping_master.apply_async(all_workers=True)

    def request_worker_method_list(self, worker_id):
        tasks.worker.send_method_list.apply_async(worker_id=worker_id)

    def receive_worker_method_list(self, worker_id, method_list):
        log.info("{0} methods: {1}".format(worker_id, method_list))

    def call_worker_method_by_name(self, worker_id, method):
        tasks.worker.call_method_by_name.apply_async(worker_id=worker_id, args=[method])
