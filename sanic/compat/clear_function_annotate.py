# ff:func feature=compat type=util control=iteration dimension=1
# ff:what Clears __annotate__ on functions for Python 3.14+ pickle compatibilit
import sys

PYTHON_314_OR_LATER = sys.version_info >= (3, 14)


def clear_function_annotate(*funcs):
    """Clear __annotate__ on functions for Python 3.14+ pickle compatibility.

    In Python 3.14, PEP 649 adds __annotate__ to functions with annotations.
    When methods are used in functools.partial and pickled, the __annotate__
    function can cause PicklingError because pickle cannot locate it by name.

    This function sets __annotate__ to None on the given functions to avoid
    pickle issues.
    """
    if not PYTHON_314_OR_LATER:
        return
    for func in funcs:
        if hasattr(func, "__annotate__") and func.__annotate__ is not None:
            func.__annotate__ = None
