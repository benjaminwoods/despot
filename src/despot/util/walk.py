import os

from pathlib import Path
from types import ModuleType


def walkdir(root, suf):
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


def walkmodule(module, skip_internal=True, skip_private=True,
               find_attr=False):
    # Walk through package/module
    _cache = []

    for handle in dir(module):
        if skip_internal:
            # Skip all handles that begin with _
            if len(handle) >= 1:
                if handle[:1] == '_':
                    continue
        elif skip_private:
            # Skip all handles that begin with __
            if len(handle) >= 2:
                if handle[:2] == '__':
                    continue

        obj = getattr(module, handle)

        # If not a module
        if not isinstance(obj, ModuleType):
            # If the object is imported from another module,
            # skip it if it is not a Python inbuilt type
            cond = (hasattr(obj, '__module__')
                    and obj.__module__ != module.__name__)
            if cond:
                continue

            if find_attr:
                # If the object is a class,
                # look for attributes + descriptors
                if isinstance(obj, type):
                    for attr in dir(obj):
                        if skip_internal:
                            # Skip all attrs that begin with _
                            if len(attr) >= 1:
                                if attr[:1] == '_':
                                    continue
                        elif skip_private:
                            # Skip all attrs that begin with _
                            if len(attr) >= 2:
                                if attr[:2] == '__':
                                    continue

                        # Scan the MRO and ignore all methods which
                        # are inherited and not overwritten
                        try:
                            for cls in obj.__mro__[1:]:
                                cond = (getattr(cls, attr, None)
                                        is getattr(obj, attr))
                                if cond:
                                    assert 0
                        except AssertionError:
                            continue

                        name = '::'.join((module.__name__, handle, attr))
                        yield Path(module.__file__), name

            # Craft name from module.__name__ and the handle
            name = '::'.join((module.__name__, handle))

            # If the name is not in the cache, skip
            if name in _cache:
                continue

            _cache.append(name)
            yield Path(module.__file__), name

        # If the object is a mod itself
        if isinstance(obj, ModuleType):
            modulename = '.'.join(obj.__name__.split('.')[:-1])

            # if it is a submodule of module,
            if modulename == module.__name__:
                # walk through the module
                for p, name in walkmodule(obj,
                                          skip_internal=skip_internal,
                                          skip_private=skip_private,
                                          find_attr=find_attr):
                    # If the name is not in the cache, skip
                    if name in _cache:
                        continue

                    _cache.append(name)
                    yield p, name
