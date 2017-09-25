import logging

from pike.manager import PikeManager

from distribrewed_core import settings

log = logging.getLogger(__name__)

_master_plugin = None
_worker_plugin = None


def clear_plugins():
    """ For testing """
    global _master_plugin
    global _worker_plugin
    _master_plugin = None
    _worker_plugin = None


def get_master_plugin():
    global _master_plugin
    if _master_plugin is None and settings.MASTER_PLUGIN_CLASS is not None:
        _master_plugin = load_plugin_class(
            'master',
            settings.PLUGIN_DIR,
            settings.MASTER_PLUGIN_CLASS
        )
    return _master_plugin


def get_worker_plugin():
    global _worker_plugin
    if _worker_plugin is None and settings.WORKER_PLUGIN_CLASS is not None:
        _worker_plugin = load_plugin_class(
            'worker',
            settings.PLUGIN_DIR,
            settings.WORKER_PLUGIN_CLASS
        )
    return _worker_plugin


def load_plugin_class(plugin_type, plugin_dir, plugin_classes):
    loaded_plugins = []
    plugin_classes = plugin_classes.split(',')
    log.debug("Searching dir '{0}' for {1} plugins...".format(plugin_dir, plugin_type))
    with PikeManager([plugin_dir]) as mgr:
        found_classes = mgr.get_classes()
        class_names = [c.__name__ for c in found_classes]
        log.debug("Found classes: {0}".format(class_names))
        for p in plugin_classes:
            log.debug("Loading plugin class '{0}'".format(p))
            if p not in class_names:
                log.debug("Plugin class {0} not found! skipping...".format(p))
            else:
                loaded_plugins.append(found_classes[class_names.index(p)]())
    if len(loaded_plugins) != 1:
        log.error("No plugin found, exiting!")
        exit(-1)
    return loaded_plugins[0] if len(loaded_plugins) == 1 else None
