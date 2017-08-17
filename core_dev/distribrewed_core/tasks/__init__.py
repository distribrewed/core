import os

from distribrewed_core.base import load_plugins

master_plugin_class = os.environ.get('MASTER_PLUGIN_CLASS', None)
master_plugin = None

if master_plugin_class is not None and master_plugin is None:
    master_plugin = load_plugins(
        'master',
        os.environ.get(
            'PLUGIN_DIR',
            os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../base'))
        ),
        master_plugin_class
    )

worker_plugin_class = os.environ.get('WORKER_PLUGIN_CLASS', None)
worker_plugin = None

if worker_plugin_class is not None and worker_plugin is None:
    worker_plugin = load_plugins(
        'worker',
        os.environ.get(
            'PLUGIN_DIR',
            os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../base'))
        ),
        worker_plugin_class
    )
