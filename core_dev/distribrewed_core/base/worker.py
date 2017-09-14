import inspect
import logging
import os

from prometheus_client import Counter

from distribrewed_core import tasks
from distribrewed_core.base.celery import CeleryWorker

log = logging.getLogger(__name__)

CALLS_TO_MASTER = Counter('CALLS_TO_MASTER', 'Number of calls to master')


# noinspection PyMethodMayBeStatic
class BaseWorker(CeleryWorker):
    def __init__(self):
        self.name = os.environ.get('WORKER_NAME', os.environ.get('HOSTNAME', None))

    def worker_info(self):
        return {
            'id': self.name,
            'ip': self.ip,
            'type': self.__class__.__name__,
            'prometheus_scrape_port': self.prom_port
        }

    def on_ready(self):
        super(BaseWorker, self).on_ready()
        log.info('Sending registration to master')
        self.call_master_method('register_worker', args=[self.name, self.worker_info()])

    def on_shutdown(self):
        super(BaseWorker, self).on_shutdown()
        log.info('Sending de-registration to master')
        self.call_master_method('de_register_worker', args=[self.name, self.worker_info()])

    def call_master_method(self, method='NONAME', args=[]):
        tasks.master.call_method_by_name.apply_async(args=[method] + args)
        CALLS_TO_MASTER.inc()

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

    def info(self):
        return 'name:{0}, type:{1}'.format(self.name, str(self.__class__.__name__))

    def start(self, shcedule):
        pass

    def stop(self):
        pass

    def pause(self):
        pass

    def resume(self):
        pass

