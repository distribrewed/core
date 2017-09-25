from unittest import TestCase
from unittest.mock import patch

from distribrewed_core.base.celery import CeleryWorker


class TestRun(TestCase):
    @patch('distribrewed_core.base.celery.start_http_server')
    @patch('distribrewed_core.base.celery.settings')
    def test_on_ready(self, settings, mock_prom_server):
        settings.AMQP_HOST = '127.0.0.1'
        settings.AMQP_PORT = 0
        settings.PROMETHEUS_SCRAPE_PORT = 9123

        worker = CeleryWorker()
        worker._on_ready()

        self.assertEqual(worker.ip, '127.0.0.1')
        self.assertEqual(worker.prom_port, settings.PROMETHEUS_SCRAPE_PORT)
        mock_prom_server.assert_called_with(settings.PROMETHEUS_SCRAPE_PORT)

    @patch('distribrewed_core.base.celery.start_http_server')
    @patch('distribrewed_core.base.celery.settings')
    def test_on_ready_fail(self, settings, mock_prom_server):
        settings.AMQP_HOST = '172.0.0.1'
        settings.AMQP_PORT = 0
        settings.PROMETHEUS_SCRAPE_PORT = 9123

        mock_prom_server.side_effect = Exception('Test prometheus server fail on')
        worker = CeleryWorker()
        worker._on_ready()

        mock_prom_server.assert_called_with(settings.PROMETHEUS_SCRAPE_PORT)

    def test_on_shutdown(self):
        worker = CeleryWorker()
        worker._on_shutdown()
