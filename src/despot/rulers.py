from importlib import import_module
from base64 import urlsafe_b64encode
from os import urandom

from importlib.machinery import SourceFileLoader
from types import FunctionType

from .util import walkdir

def nero(path,name,testdir,language):
    # Nero
    # x 1) Tests must exist for all functions and classes, in any test file
    # o 2) Base object must be explicitly imported at the module level, in
    #      the test module
    
    # Split my.module::obj::nestedobj::method
    # into (my.module, (obj, nestedobj, method))
    spl = name.split('::')
    modulename, objname_withscope = spl[0], spl[1:]
    
    # Split obj::nestedobj::method into (obj, (nestedobj, method))
    base_objname, attrs = objname_withscope[0], objname_withscope[1:]
    
    # Get my.module, then get obj from my.module
    module = import_module(modulename)
    baseobj = getattr(module, base_objname)
    
    # Deep dive by iterating through attrs
    # to get obj.nestedobj.method
    obj = baseobj
    for attr in attrs:
        obj = getattr(obj, attr)
    objname = base_objname if attrs == [] else attr
    
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

    passing = [False, False]
    for t in walkdir(testdir,'.py'):
        if not all(passing):
            # Test 1
            rand_modname = urlsafe_b64encode(urandom(12))
            rand_modname = rand_modname.decode('utf-8')
            loader = SourceFileLoader(rand_modname, str(t.absolute()))
            _testmod = loader.load_module(rand_modname)
            
            testobj = getattr(_testmod, f'{prefix}_{objname}', None)
            if objtype == 'class':
                if isinstance(testobj, type):
                    passing[0] = True
            elif objtype == 'function':
                if isinstance(testobj, FunctionType):
                    passing[0] = True
            
            # Test 2
            if passing[0]:
                # Loop through all obj in the test module
                for obj in map(lambda x: getattr(_testmod, x), dir(_testmod)):
                    # Identity check
                    if obj is baseobj:
                        passing[1] = True
                        break
    if not all(passing):
        raise AssertionError(f'No test found for {name}.')