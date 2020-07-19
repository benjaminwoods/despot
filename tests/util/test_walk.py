from importlib import import_module
from shutil import rmtree
import sys

import pytest

from despot.util.walk import walkdir, walkmodule


@pytest.fixture
def tempPackage(tmp_path, scope='module'):
    # Structure:
    # └── test_pkg
    #     |── subpkg0
    #     |   |── __init__.py
    #     |   └── mod0.py
    #     |   └── mod1.py
    #     |── subpkg1
    #     |   |── __init__.py
    #     |   └── mod0.py
    #     |   └── mod1.py
    #     |── temp.txt
    #     └── __init__.py

    d = tmp_path / "test_pkg"
    d.mkdir()
    for i in range(2):
        subpkg = d / f"subpkg{i}"
        subpkg.mkdir()
        filepath = subpkg / '__init__.py'
        filepath.write_text(f'from . import mod{2*i}, mod{2*i+1}')
        for j in range(2):
            filepath = subpkg / f'mod{2*i+j}.py'
            filepath.write_text(f'def my_func{2*i+j}():\n'
                                '\tpass\n'
                                '\n\n'
                                f'class my_class{2*i+j}:\n'
                                f'\tdef my_method{2*i+j}(self):\n'
                                f'\t\treturn {2*i+j}')
    (d / "__init__.py").write_text(f'from . import subpkg0, subpkg1')
    (d / "temp.txt").touch()

    # Modify sys path for ease
    sys.path.append(str(d.parent))

    # Yield path to the package
    yield d
    
    # Teardown
    sys.path.remove(str(d.parent))
    rmtree(str(d))


def test_walkdir(tempPackage):
    outputs = [tempPackage / '__init__.py',
               tempPackage / 'subpkg0' / 'mod0.py',
               tempPackage / 'subpkg0' / 'mod1.py',
               tempPackage / 'subpkg0' / '__init__.py',
               tempPackage / 'subpkg1' / 'mod2.py',
               tempPackage / 'subpkg1' / 'mod3.py',
               tempPackage / 'subpkg1' / '__init__.py']

    # Test for .py
    for i in walkdir(tempPackage, '.py'):
        assert i in outputs

    # Test for .txt
    assert list(walkdir(tempPackage, '.txt')) == [tempPackage / 'temp.txt']

    # Test for .c (no files)
    assert list(walkdir(tempPackage, '.c')) == []


def test_walkmodule(tempPackage):
    pkg_name = tempPackage.absolute().stem

    test_pkg = import_module(pkg_name)

    paths = (tempPackage / 'subpkg0' / 'mod0.py',
             tempPackage / 'subpkg0' / 'mod0.py',
             tempPackage / 'subpkg0' / 'mod1.py',
             tempPackage / 'subpkg0' / 'mod1.py',
             tempPackage / 'subpkg1' / 'mod2.py',
             tempPackage / 'subpkg1' / 'mod2.py',
             tempPackage / 'subpkg1' / 'mod3.py',
             tempPackage / 'subpkg1' / 'mod3.py')

    names = ('test_pkg.subpkg0.mod0::my_class0',
             'test_pkg.subpkg0.mod0::my_func0',
             'test_pkg.subpkg0.mod1::my_class1',
             'test_pkg.subpkg0.mod1::my_func1',
             'test_pkg.subpkg1.mod2::my_class2',
             'test_pkg.subpkg1.mod2::my_func2',
             'test_pkg.subpkg1.mod3::my_class3',
             'test_pkg.subpkg1.mod3::my_func3')

    outputs = list(zip(paths, names))

    for i in walkmodule(test_pkg):
        assert i in outputs
