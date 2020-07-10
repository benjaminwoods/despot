from importlib import import_module
from base64 import urlsafe_b64encode
from os import urandom

from importlib.machinery import SourceFileLoader
from types import FunctionType

from .util import walkdir

def nero(path,name,testdir,language):
    """
    Nero.
    
    Checks that callables have unit tests.
    
    Requirements for passing:
        - The callable given by `name` must have a unit test with a compliant
          name, in any source file in the test directory
        - If the callable exists in the global namespace, it must be
          explicitly imported in the global namespace in the test source file

    Language requirements:
        - If the language is Python, this test must be a pytest unit test
        - (No support for other languages yet!)
    """
    
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
    objname = '.'.join(objname_withscope)
    
    if not callable(obj):
        # Only check callable objects for tests
        return
    
    # testname
    if isinstance(obj, type):
        # If a class or metaclass
        testname = f'Test_{objname}'
        objtype = 'class'
    elif isinstance(obj, FunctionType):
        # If a function
        testname = f'test_{objname}'
        objtype = 'function'
    else:
        objtype = 'function'
    
    # If attribute of a class, override testname
    if len(objname_withscope) > 1:
        _start = '::'.join(map(lambda x: f'Test_{x}',
                              objname_withscope[:-1]))
        testname = f'{_start}::test_{objname_withscope[-1]}'
    
    passing = [False, False]
    for t in walkdir(testdir,'.py'):
        if not all(passing):
            # Test 1
            rand_modname = urlsafe_b64encode(urandom(12))
            rand_modname = rand_modname.decode('utf-8')
            loader = SourceFileLoader(rand_modname, str(t.absolute()))
            _testmod = loader.load_module(rand_modname)
            
            testobj = _testmod
            for attr in testname.split('::'):
                if not hasattr(testobj, attr):
                    break
                testobj = getattr(testobj, attr)
            
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