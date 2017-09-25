from unittest import TestCase
from unittest.mock import patch

from distribrewed_core import settings as default_settings
from distribrewed_core.plugin import get_worker_plugin, get_master_plugin, clear_plugins


class Tests(TestCase):
    def setUp(self):
        clear_plugins()

    @patch('distribrewed_core.plugin.exit')
    @patch('distribrewed_core.plugin.settings')
    def test_load_base_master_plugin_not_found(self, settings, exit):
        settings.MASTER_PLUGIN_CLASS = 'NotFound'
        settings.PLUGIN_DIR = default_settings.PLUGIN_DIR
        m = get_master_plugin()
        exit.assert_called_with(-1)
        self.assertEqual(m, None)

    @patch('distribrewed_core.plugin.settings')
    def test_load_base_master_plugin(self, settings):
        clear_plugins()
        settings.MASTER_PLUGIN_CLASS = 'BaseMaster'
        settings.PLUGIN_DIR = default_settings.PLUGIN_DIR
        m = get_master_plugin()
        self.assertEqual(m.__class__.__name__, 'BaseMaster')

    @patch('distribrewed_core.plugin.settings')
    def test_load_base_worker_plugin(self, settings):
        clear_plugins()
        settings.WORKER_PLUGIN_CLASS = 'BaseWorker'
        settings.PLUGIN_DIR = default_settings.PLUGIN_DIR
        w = get_worker_plugin()
        self.assertEqual(w.__class__.__name__, 'BaseWorker')
