from unittest import TestCase
from unittest.mock import patch

from distribrewed_core.base.celery import get_ip


class TestRun(TestCase):

    def setUp(self):
        self.env = {
            'AMQP_HOST': '127.0.0.1'
        }

    def test_run_task(self):
        with patch.dict('os.environ', self.env):
            get_ip()
