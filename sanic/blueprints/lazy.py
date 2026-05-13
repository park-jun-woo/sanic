# ff:func feature=blueprint type=util control=sequence
# ff:what Decorator to register a function to be called later on blueprint regi
from __future__ import annotations

from functools import wraps
from inspect import isfunction


def lazy(func, as_decorator=True):
    """Decorator to register a function to be called later.

    Args:
        func (Callable): Function to be called later.
        as_decorator (bool): Whether the function should be called
            immediately or not.
    """

    @wraps(func)
    def decorator(bp, *args, **kwargs):
        nonlocal as_decorator
        kwargs["apply"] = False
        pass_handler = None

        if args and isfunction(args[0]):
            as_decorator = False

        def wrapper(handler):
            future = func(bp, *args, **kwargs)
            if as_decorator:
                future = future(handler)

            if bp.registered:
                for app in bp.apps:
                    bp.register(app, {})

            return future

        return wrapper if as_decorator else wrapper(pass_handler)

    return decorator
