import pytest

@pytest.mark.xfail
def test_register():
    pass

@pytest.mark.xfail
def test_walkdir():
    pass

@pytest.mark.xfail
def test_walkmodule():
    pass

@pytest.mark.xfail
class Test_Singleton():
    pass

@pytest.mark.xfail
class Test_ABCSingletonMeta():
    pass

@pytest.mark.xfail
class Test__RulerRegistry():
    pass

@pytest.mark.xfail
class Test__DespotRegistry():
    pass