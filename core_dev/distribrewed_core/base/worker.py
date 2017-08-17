import inspect
import logging
import os

from distribrewed_core import tasks

log = logging.getLogger(__name__)


# noinspection PyMethodMayBeStatic
class BaseWorker:
    def __init__(self):
        self.name = os.environ.get('WORKER_NAME', os.environ.get('HOSTNAME', None))

    def call_master_method(self, method='NONAME', args=[]):
        tasks.master.call_method_by_name.apply_async(args=[method] + args)

    def ping_master(self):
        log.info('Sending ping to master')
        self.call_master_method('handle_ping', args=[self.name])

    def handle_ping(self):
        log.info('Received ping from master')
        log.info('Sending pong to master')
        self.call_master_method('handle_pong', args=[self.name])

    def handle_pong(self):
        log.info('Received pong from master')

    def send_method_list(self):
        log.info('Sending methods to master')
        methodList = [e for e in dir(self) if callable(getattr(self, e)) and not e.startswith('__')]
        self.call_master_method('receive_worker_method_list', args=[self.name, methodList])

    def send_method_parameter_list(self, method_name):
        log.info('Sending parameter list of method \'{0}\' to master'.format(method_name))
        parameterList = inspect.signature(getattr(self, method_name))
        self.call_master_method('receive_worker_method_parameter_list', args=[
            self.name,
            method_name,
            parameterList
        ])
