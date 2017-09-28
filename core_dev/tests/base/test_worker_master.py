from unittest import TestCase
from unittest.mock import patch

from distribrewed_core import settings as default_settings
from distribrewed_core.plugin import get_master_plugin, get_worker_plugin, clear_plugins


def worker_method_by_name(*args, **kwargs):
    method = kwargs.get('args')[0]
    a = tuple(kwargs.get('args')[1:])
    getattr(get_worker_plugin(), method)(*a)


def master_method_by_name(*args, **kwargs):
    method = kwargs.get('args')[0]
    a = tuple(kwargs.get('args')[1:])
    getattr(get_master_plugin(), method)(*a)


class Tests(TestCase):
    @patch(
        'distribrewed_core.tasks.worker.call_method_by_name.apply_async',
        create=True,
        side_effect=worker_method_by_name
    )
    @patch(
        'distribrewed_core.tasks.master.call_method_by_name.apply_async',
        create=True,
        side_effect=master_method_by_name
    )
    @patch('distribrewed_core.plugin.settings')
    def test_ping(self, settings, master_task, worker_task):
        settings.MASTER_PLUGIN_CLASS = 'BaseMaster'
        settings.WORKER_PLUGIN_CLASS = 'BaseWorker'
        settings.WORKER_NAME = default_settings.WORKER_NAME
        settings.PLUGIN_DIR = default_settings.PLUGIN_DIR

        clear_plugins()

        m = get_master_plugin()
        w = get_worker_plugin()
        m.ping_worker(settings.WORKER_NAME)

        worker_task.assert_called_with(all_workers=None, args=['_handle_ping'], worker_id=default_settings.WORKER_NAME)
        master_task.assert_called_with(args=['_handle_pong', default_settings.WORKER_NAME])

    @patch(
        'distribrewed_core.tasks.worker.call_method_by_name.apply_async',
        create=True,
        side_effect=worker_method_by_name
    )
    @patch(
        'distribrewed_core.tasks.master.call_method_by_name.apply_async',
        create=True,
        side_effect=master_method_by_name
    )
    @patch('distribrewed_core.plugin.settings')
    def test_ping_all(self, settings, master_task, worker_task):
        settings.MASTER_PLUGIN_CLASS = 'BaseMaster'
        settings.WORKER_PLUGIN_CLASS = 'BaseWorker'
        settings.WORKER_NAME = default_settings.WORKER_NAME
        settings.PLUGIN_DIR = default_settings.PLUGIN_DIR

        clear_plugins()

        m = get_master_plugin()
        w = get_worker_plugin()
        m.command_all_workers_to_ping_master()
        master_task.assert_called_with(args=['_handle_ping', default_settings.WORKER_NAME])
        worker_task.assert_called_with(all_workers=False, args=['_handle_pong'], worker_id=default_settings.WORKER_NAME)
