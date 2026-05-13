# ff:func feature=util type=util control=sequence
# ff:what Imports a module or class by its dotted string path
from importlib import import_module
from inspect import ismodule


def import_string(module_name, package=None):
    """
    import a module or class by string path.

    :module_name: str with path of module or path to import and
    instantiate a class
    :returns: a module object or one instance from class if
    module_name is a valid path to class

    """
    module, klass = module_name.rsplit(".", 1)
    module = import_module(module, package=package)
    obj = getattr(module, klass)
    if ismodule(obj):
        return obj
    return obj()
