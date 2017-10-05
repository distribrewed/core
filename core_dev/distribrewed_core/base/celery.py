import logging
import socket

from prometheus_client import start_http_server

from distribrewed_core import settings

log = logging.getLogger(__name__)


def get_ip():
    if settings.PROMETHEUS_SCRAPE_IP:
        return settings.PROMETHEUS_SCRAPE_IP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((settings.AMQP_HOST, settings.AMQP_PORT))
    ip = s.getsockname()[0]
    s.close()
    return ip


class CeleryWorker:
    prom_port = None
    ip = None

    # noinspection PyMethodMayBeStatic
    def _on_ready(self):
        try:
            self.prom_port = settings.PROMETHEUS_SCRAPE_PORT
            log.info('Starting prometheus scrape port on {0}'.format(self.prom_port))
            start_http_server(self.prom_port)
        except Exception as e:
            log.error('Failed starting prometheus scrape port: {0}'.format(e))

        self.ip = get_ip()
        if self.ip.startswith('172'):
            log.warning('Container not running in HOST mode, not a public IP address')

    def _on_shutdown(self):
        pass
