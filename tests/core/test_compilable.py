import pytest

from skeema.core.compilable import Compilable


class MyCompilable(Compilable):
    def _compile(self, compilation_context):
        pass

    def _find_dependencies(self):
        return []


@pytest.fixture(name="compilable")
def test_compilable():
    return MyCompilable()


class TestCompilable:
    class TestCompile:
        def test_sets_compiled_to_true(self, compilable):
            compilable.compile()
            assert compilable.compiled is True
