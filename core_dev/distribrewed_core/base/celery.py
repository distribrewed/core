import logging
import os
import socket

from prometheus_client import start_http_server

log = logging.getLogger(__name__)


def get_ip():
    return socket.gethostbyname(socket.gethostname())


class CeleryWorker:
    prom_port = None
    ip = None

    # noinspection PyMethodMayBeStatic
    def on_ready(self):
        try:
            self.prom_port = int(os.environ.get('PROMETHEUS_SCRAPE_PORT', '9000'))
            log.info('Starting prometheus scrape port on {0}'.format(self.prom_port))
            start_http_server(self.prom_port)
        except Exception as e:
            log.error('Failed starting prometheus scrape port: {0}'.format(e))

        self.ip = get_ip()
        if self.ip.startswith('172'):
            log.warning('Container not running in HOST mode, not a public IP address')

    def on_shutdown(self):
        pass
