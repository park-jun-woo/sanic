# ff:type feature=touchup type=manager
# ff:what Service class that applies AST-based code transformations to register


from inspect import getmembers, getmodule

from .schemes import BaseScheme


class TouchUp:
    _registry: set[tuple[type, str]] = set()

    @classmethod
    def _resolve_method(cls, target, method_name, app):
        method = getattr(target, method_name)
        if not app.test_mode:
            return method
        placeholder = f"_{method_name}"
        if hasattr(target, placeholder):
            return getattr(target, placeholder)
        setattr(target, placeholder, method)
        return method

    @classmethod
    def run(cls, app):
        for target, method_name in cls._registry:
            method = cls._resolve_method(target, method_name, app)
            module = getmodule(target)
            module_globals = dict(getmembers(module))
            modified = BaseScheme.build(method, module_globals, app)
            setattr(target, method_name, modified)
            target.__touched__ = True

    @classmethod
    def register(cls, target, method_name):
        cls._registry.add((target, method_name))
