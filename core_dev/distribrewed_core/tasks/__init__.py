import os

from distribrewed_core.base import load_plugins

master_plugin = None
if master_plugin is None:
    master_plugin = load_plugins(
        'master',
        os.environ.get('PLUGIN_DIR',
                       os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../base'))),
        os.environ.get('MASTER_PLUGIN_CLASSES', 'BaseMaster')
    )[0]  # TODO: FIX

worker_plugin = None
if worker_plugin is None:
    worker_plugin = load_plugins(
        'worker',
        os.environ.get('PLUGIN_DIR',
                       os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../base'))),
        os.environ.get('WORKER_PLUGIN_CLASSES', 'BaseWorker')
    )[0]  # TODO: FIX
