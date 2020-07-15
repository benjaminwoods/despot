from abc import ABCMeta
from collections import abc
import pytest

from despot import classes
from despot import rulers
from despot.util.reg import (register, Singleton, ABCSingletonMeta,
                             _RulerRegistry, _DespotRegistry)


@pytest.fixture
def SingletonClass():
    class myClass(metaclass=Singleton):
        pass

    yield myClass


@pytest.fixture
def DespotReg():
    # Shallow copy into dict
    reg = _DespotRegistry()
    d = {**reg}

    yield reg

    reg.clear()
    reg.update(d)


@pytest.fixture
def RulerReg():
    # Shallow copy into dict
    reg = _RulerRegistry()
    d = {**reg}

    yield reg

    reg.clear()
    reg.update(d)


@pytest.fixture
def MyDespot():
    class MyDespot(classes.Despot):
        pass
    return MyDespot


@pytest.fixture
def MyRuler():
    def MyRuler(path, name, language, **options):
        pass
    return MyRuler


def test_register(DespotReg, RulerReg,
                  MyDespot, MyRuler):
    # Despot
    assert MyDespot not in DespotReg
    register(MyDespot, 'pass')
    assert 'pass' in DespotReg
    assert DespotReg['pass'] == MyDespot

    with pytest.raises(ValueError):
        register(dict, 'fail')

    # Despot
    assert MyRuler not in RulerReg
    register(MyRuler, 'pass')
    assert 'pass' in RulerReg
    assert RulerReg['pass'] == MyRuler

    with pytest.raises(ValueError):
        register(lambda x: 0, 'fail')


class Test_Singleton:
    def test_uniqueness(self, SingletonClass):
        assert SingletonClass() is SingletonClass()

    def test_implementation(self, SingletonClass):
        assert SingletonClass not in Singleton._instances
        SingletonClass()
        assert SingletonClass in Singleton._instances


class Test_ABCSingletonMeta:
    def test_mro(self):
        assert ABCSingletonMeta.__mro__ == (ABCSingletonMeta,
                                            ABCMeta,
                                            Singleton,
                                            type,
                                            object)


class Test__RulerRegistry:
    def test_type(self, RulerReg):
        assert isinstance(_RulerRegistry, Singleton)

        assert isinstance(RulerReg, abc.MutableMapping)

    def test_items(self, RulerReg):
        d = {'nero': rulers.nero,
             'cleopatra': rulers.cleopatra,
             'joan': rulers.joan}

        for k, v in d.items():
            assert RulerReg.get(k, None) is v
        for k, v in RulerReg.items():
            assert d.get(k, None) is v

    def test_setitem(self, RulerReg, MyRuler):
        RulerReg['pass'] = MyRuler
        assert RulerReg['pass'] == MyRuler

        with pytest.raises(ValueError):
            RulerReg['fail'] = (lambda x: 0)


class Test__DespotRegistry():
    def test_type(self, DespotReg):
        assert isinstance(_DespotRegistry, Singleton)

        assert isinstance(DespotReg, abc.MutableMapping)

    def test_items(self, DespotReg):
        d = {'Despot': classes.Despot}

        for k, v in d.items():
            assert DespotReg.get(k, None) is v
        for k, v in DespotReg.items():
            assert d.get(k, None) is v

    def test_setitem(self, DespotReg, MyDespot):
        DespotReg['pass'] = MyDespot
        assert DespotReg['pass'] == MyDespot

        with pytest.raises(ValueError):
            DespotReg['fail'] = dict
