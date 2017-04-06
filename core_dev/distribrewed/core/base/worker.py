import logging
import os

from distribrewed import core

log = logging.getLogger(__name__)


class BaseWorker:
    def __init__(self):
        self.name = os.environ.get('WORKER_NAME', None)

    def ping_master(self):
        log.info('Sending ping to master')
        core.tasks.master.handle_ping.apply_async(args=[self.name])

    def handle_ping(self):
        log.info('Received ping from master')
        log.info('Sending pong to master')
        core.tasks.master.handle_pong.apply_async(args=[self.name])

    # noinspection PyMethodMayBeStatic
    def handle_pong(self):
        log.info('Received pong from master')

    def send_method_list(self):
        log.info('Sending methods')
        methodList = [e for e in dir(self) if callable(getattr(self, e)) and not e.startswith('__')]
        core.tasks.master.receive_worker_method_list.apply_async(args=[self.name, methodList])
