from importlib import import_module
from base64 import urlsafe_b64encode
from os import urandom

from importlib.machinery import SourceFileLoader
from types import FunctionType

from .util import walkdir

def nero(name,testdir,language):
    # Nero
    # x 1) Tests must exist for all functions and classes, in any test file
    # o 2) Callables must be explicitly imported at the module level, in
    #      the test module
    
    spl = name.split('.')
    modulename, objname = '.'.join(spl[:-1]), spl[-1]
    module = import_module(modulename)
    obj = getattr(module, objname)
    
    if not callable(obj):
        # Only check callable objects for tests
        return
    else:
        if isinstance(obj, type):
            # If a class or metaclass
            prefix = 'Test'
            objtype = 'class'
        elif isinstance(obj, FunctionType):
            # If a function
            prefix = 'test'
            objtype = 'function'
    
    found = False
    for t in walkdir(testdir,'.py'):
        rand_modname = urlsafe_b64encode(urandom(12))
        rand_modname = rand_modname.decode('utf-8')
        loader = SourceFileLoader(rand_modname, str(t.absolute()))
        _testmod = loader.load_module(rand_modname)
        
        testobj = getattr(_testmod, f'{prefix}_{objname}', None)
        if objtype == 'class':
            if isinstance(testobj, type):
                found = True
                break
        if objtype == 'function':
            if isinstance(testobj, FunctionType):
                found = True
                break
    if not found:
        raise AssertionError(f'No test found for {name}.')