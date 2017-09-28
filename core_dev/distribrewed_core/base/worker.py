import datetime
import inspect
import logging
from collections import OrderedDict
from threading import Thread
from time import sleep

import schedule
from prometheus_client import Counter

from distribrewed_core import tasks, settings
from distribrewed_core.base.celery import CeleryWorker

log = logging.getLogger(__name__)


# noinspection PyMethodMayBeStatic
class BaseWorker(CeleryWorker):
    def __init__(self):
        self.name = settings.WORKER_NAME
        try:
            BaseWorker.CALLS_TO_MASTER = Counter('CALLS_TO_MASTER', 'Number of calls to master')
        except ValueError:
            pass  # It is already defined

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
        self.CALLS_TO_MASTER.inc()

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


# Schedule workers

scheduler_running = False
scheduler_paused = False


def run_scheduler():
    global scheduler_running
    global scheduler_paused
    while scheduler_running:
        if not scheduler_paused:
            schedule.run_pending()
        sleep(1)


class ScheduleWorker(BaseWorker):
    schedule_thread = None

    def __init__(self):
        super(ScheduleWorker, self).__init__()

    def _setup_worker_schedule(self, worker_schedule):
        """
        Override this method when creating schedule workers
        """
        pass

    def start_worker(self, worker_schedule):
        schedule.clear()
        self._setup_worker_schedule(worker_schedule)
        global scheduler_running
        if not scheduler_running:
            scheduler_running = True
            self.schedule_thread = Thread(target=run_scheduler)
            self.schedule_thread.start()
        self.resume_worker()

    def stop_worker(self):
        global scheduler_running
        if scheduler_running:
            scheduler_running = False
            self.schedule_thread.join(timeout=10)
            self.schedule_thread = None

    # noinspection PyMethodMayBeStatic
    def pause_worker(self):
        global scheduler_paused
        scheduler_paused = True

    # noinspection PyMethodMayBeStatic
    def resume_worker(self):
        global scheduler_paused
        scheduler_paused = False

    def send_status_to_master(self):
        global scheduler_running
        global scheduler_paused
        self._call_master_method(method='_handle_status_from_worker', args=[
            self.name,
            scheduler_running,
            scheduler_paused
        ])
