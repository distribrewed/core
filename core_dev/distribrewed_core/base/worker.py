import datetime
import inspect
import logging
from collections import OrderedDict

from prometheus_client import Counter

from distribrewed_core import tasks, settings
from distribrewed_core.base.celery import CeleryWorker

log = logging.getLogger(__name__)

CALLS_TO_MASTER = Counter('CALLS_TO_MASTER', 'Number of calls to master')


# noinspection PyMethodMayBeStatic
class BaseWorker(CeleryWorker):
    def __init__(self):
        self.name = settings.WORKER_NAME

    def _worker_info(self):
        return {
            'id': self.name,
            'ip': self.ip,
            'type': self.__class__.__name__,
            'prometheus_scrape_port': self.prom_port
        }

    def _worker_methods(self):
        methods = [e for e in dir(self) if callable(getattr(self, e)) and not e.startswith('_')]
        res = {}
        for m in methods:
            params = OrderedDict(inspect.signature(getattr(self, m)).parameters)
            d = ()
            for k, v in params.items():
                d += (str(v),)
            res[m] = d
        return res

    def _on_ready(self):
        super(BaseWorker, self)._on_ready()
        self.register()

    def _on_shutdown(self):
        super(BaseWorker, self)._on_shutdown()
        self.de_register()

    def _call_master_method(self, method='NONAME', args=[]):
        tasks.master.call_method_by_name.apply_async(args=[method] + args)
        CALLS_TO_MASTER.inc()

    # Registration methods

    def register(self):
        log.info('Sending registration to master')
        self._call_master_method('_register_worker', args=[self.name, self._worker_info(), self._worker_methods()])

    def de_register(self):
        log.info('Sending de-registration to master')
        self._call_master_method('_de_register_worker', args=[self.name, self._worker_info()])

    # Ping methods

    def ping_master(self):
        log.info('Sending ping to master')
        self._call_master_method('_handle_ping', args=[self.name])

    def _handle_ping(self):
        log.info('Received ping from master')
        log.info('Sending pong to master')
        self._call_master_method('_handle_pong', args=[self.name])

    def _handle_pong(self):
        log.info('Received pong from master')

    # Time sync

    def _handle_time_sync_request(self, current_master_time):
        current_master_time = datetime.datetime.strptime(current_master_time, "%Y-%m-%dT%H:%M:%S.%f")
        log.info('Received time from master: {0}'.format(current_master_time))
        diff = datetime.datetime.now() - current_master_time
        if diff > datetime.timedelta(seconds=5):
            # TODO: Something more than a warning
            log.warning('Time diff between master and worker more than 5 seconds: {}'.format(diff))

    def time_sync(self):
        log.info('Requesting time sync with master')
        self._call_master_method('_handle_time_sync_request', args=[self.name])


class ScheduleWorker(BaseWorker):
    def __init__(self):
        super(ScheduleWorker, self).__init__()

    def start_worker(self, schedule):
        pass

    def stop_worker(self):
        pass

    def pause_worker(self):
        pass

    def resume_worker(self):
        pass
