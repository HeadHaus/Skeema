import pytest
import sys

from skeema.core.handle import INVALID_HANDLE
from skeema.core.container import Container


class MyObject:
    def on_add_to_container(self, handle, debug_name):
        pass


@pytest.fixture(name="container")
def create_container():
    container = Container()
    yield container


class TestContainer:
    class TestAddObject:
        def test_returns_valid_handle(self, container, id0):
            object_in = MyObject()
            handle = container.add_object(id0, object_in, id0)
            assert handle != INVALID_HANDLE

        def test_creates_reference(self, container, id0):
            object_in = MyObject()
            container.add_object(id0, object_in, id0)
            expected_ref_count = 2
            actual_ref_count = sys.getrefcount(object_in) - 1
            assert expected_ref_count == actual_ref_count

        def test_returns_invalid_handle_with_duplicate_id(self, container, id0):
            container.add_object(id0, MyObject(), id0)
            handle = container.add_object(id0, MyObject(), id0)
            assert handle == INVALID_HANDLE

    class TestGetObjectHandle:
        def test_returns_correct_handle_with_valid_id(self, container, id0):
            object_in = MyObject()
            handle_add = container.add_object(id0, object_in, id0)
            handle_get = container.get_object_handle(id0)
            assert handle_get == handle_add

    class TestGetObject:
        def test_does_not_create_reference(self, container, id0):
            object_in = MyObject()
            handle = container.add_object(id0, object_in, id0)
            object_out = container.get_object(handle)
            assert object_in == object_out

            expected_ref_count = 2
            actual_ref_count = sys.getrefcount(object_in) - 1
            assert expected_ref_count == actual_ref_count

        def test_returns_none_with_invalid_handle(self, container):
            object_out = container.get_object(INVALID_HANDLE)
            assert object_out is None

    class TestClear:
        def test_removes_all_objects(self, container, id0):
            object_in = MyObject()
            handle_in = container.add_object(id0, object_in, id0)
            container.clear()

            object_out = container.get_object(handle_in)
            assert object_out is None

            handle_out = container.get_object_handle(id0)
            assert handle_out == INVALID_HANDLE

            object_out = container.get_object(handle_out)
            assert object_out is None

            expected_ref_count = 1
            actual_ref_count = sys.getrefcount(object_in) - 1
            assert expected_ref_count == actual_ref_count
