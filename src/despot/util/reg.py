from collections import UserDict
from abc import ABCMeta

from types import FunctionType
from inspect import getfullargspec


def register(obj, name):
    from ..classes import Despot
    if isinstance(obj, type):
        if isinstance(obj.__new__(obj), Despot):
            _DespotRegistry()[name] = obj
            return

    try:
        _RulerRegistry()[name] = obj
    except ValueError:
        raise ValueError(f'Object {name} is neither a Despot or Ruler.')


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args,
                                                                 **kwargs)
        return cls._instances[cls]


class ABCSingletonMeta(ABCMeta, Singleton):
    pass


class _RulerRegistry(UserDict, metaclass=ABCSingletonMeta):
    def __setitem__(self, item, val):
        if not isinstance(val, FunctionType):
            raise ValueError(f'Ruler must be a function.')
        gfas = getfullargspec(val)
        cond = (gfas.args != ['path', 'name', 'language']
                or gfas.varargs is not None
                or gfas.varkw != 'options'
                or gfas.defaults is not None
                or gfas.kwonlyargs != []
                or gfas.kwonlydefaults is not None)
        if cond:
            raise ValueError(f'Ruler must adhere to signature guidelines.')
        super().__setitem__(item, val)


class _DespotRegistry(UserDict, metaclass=ABCSingletonMeta):
    def __setitem__(self, item, val):
        from ..classes import Despot
        if isinstance(val, type) and isinstance(val.__new__(val), Despot):
            super().__setitem__(item, val)
        else:
            raise ValueError(f'Only subclasses of Despot are permitted.')
