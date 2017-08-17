import os

from distribrewed_core.base import load_plugins

master_plugin = None
if master_plugin is None and os.environ.get('LOAD_MASTER_PLUGIN', 'n').lower() in ['y', 'yes', '1']:
    master_plugin = load_plugins(
        'master',
        os.environ.get('PLUGIN_DIR',
                       os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../base'))),
        os.environ.get('MASTER_PLUGIN_CLASSES', 'BaseMaster')
    )


worker_plugin = None
if worker_plugin is None and os.environ.get('LOAD_WORKER_PLUGIN', 'n').lower() in ['y', 'yes', '1']:
    worker_plugin = load_plugins(
        'worker',
        os.environ.get('PLUGIN_DIR',
                       os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../base'))),
        os.environ.get('WORKER_PLUGIN_CLASSES', 'BaseWorker')
    )
