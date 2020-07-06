import os

from pathlib import Path
from types import ModuleType
from collections import UserDict
from abc import ABCMeta

from types import FunctionType
from inspect import getfullargspec

def register(obj, name):
    from .classes import Despot
    if isinstance(obj, type):
        if isinstance(obj.__new__(obj), Despot):
            _DespotRegistry()[name] = obj
            return
    
    try:
        _RulerRegistry()[name] = obj
    except ValueError:
        raise ValueError(f'Object {name} is neither a Despot or Ruler.')

def walkdir(root,suf):
    """
    Generator. Walk through root. If file has a suffix in suf, yield.
    """

    if isinstance(suf, str):
        suf = [suf]
    for path, subdirs, files in os.walk(root):
        for name in files:
            p = Path(path, name)
            # Add logic for .gitignore
            if p.suffix in suf:
                yield p

def walkmodule(module):
    # Walk through package/module
    _cache = []
    
    for handle in dir(module):
        #if handle[0] == '_':
        #    continue
        
        obj = getattr(module,handle)
        
        # Test values?
        if not isinstance(obj, ModuleType):
            if (hasattr(obj, '__module__')
                and obj.__module__ != module.__name__):
                    continue
            
            name = '.'.join((module.__name__, handle))
            if name in _cache:
                continue
            
            _cache.append(name)
            yield name
        
        if isinstance(obj, ModuleType):
            if '.'.join(obj.__name__.split('.')[:-1]) == module.__name__: 
                for name in walkmodule(obj):
                    if name in _cache:
                        continue
                    
                    _cache.append(name)
                    yield name
        # !!! Check methods of classes

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
        if (gfas.args != ['name', 'testdir', 'language']
            or gfas.varargs is not None
            or gfas.varkw is not None
            or gfas.defaults is not None
            or gfas.kwonlyargs != []
            or gfas.kwonlydefaults is not None):
            raise ValueError(f'Ruler must adhere to signature guidelines.')
        super().__setitem__(item, val)

class _DespotRegistry(UserDict, metaclass=ABCSingletonMeta):
    def __setitem__(self, item, val):
        from .classes import Despot
        if isinstance(val, type) and isinstance(val.__new__(val), Despot):
            super().__setitem__(item, val)
        else:
            raise ValueError(f'Only subclasses of Despot are permitted.')
