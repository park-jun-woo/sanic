# ff:type feature=core type=config
# ff:what Metaclass for Config that tracks descriptor setters
from abc import ABCMeta
from inspect import getmembers, isdatadescriptor


class DescriptorMeta(ABCMeta):
    """Metaclass for Config."""

    def __init__(cls, *_):
        cls.__setters__ = {name for name, _ in getmembers(cls, cls._is_setter)}

    @staticmethod
    def _is_setter(member: object):
        return isdatadescriptor(member) and hasattr(member, "setter")
