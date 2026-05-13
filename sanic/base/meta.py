# ff:type feature=base type=model
# ff:what Metaclass for Sanic base classes that sets __slots__ to empty tuple


class SanicMeta(type):
    @classmethod
    def __prepare__(metaclass, name, bases, **kwds):
        cls = super().__prepare__(metaclass, name, bases, **kwds)
        cls["__slots__"] = ()
        return cls
