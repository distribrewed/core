from pike.manager import PikeManager


def load_plugins(plugin_type, plugin_dir, plugin_classes):
    loaded_plugins = []
    plugin_classes = plugin_classes.split(',')
    print("Searching dir '{0}' for {1} plugins...".format(plugin_dir, plugin_type), flush=True)
    with PikeManager([plugin_dir]) as mgr:
        found_classes = mgr.get_classes()
        class_names = [c.__name__ for c in found_classes]
        print("Found classes: {0}".format(class_names), flush=True)
        for p in plugin_classes:
            print("Loading plugin class '{0}'".format(p), flush=True)
            if p not in class_names:
                print("Plugin class {0} not found! skipping...".format(p))
            else:
                loaded_plugins.append(found_classes[class_names.index(p)]())
    return loaded_plugins
