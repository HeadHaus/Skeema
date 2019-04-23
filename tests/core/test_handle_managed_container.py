import pytest
import sys

from skeema.core.handle import INVALID_HANDLE
from skeema.core.handle import HandleIsInactiveException
from skeema.core.handle_managed_container import HandleManagedContainer


class MyObject:
    pass


@pytest.fixture(name="container")
def create_container():
    container = HandleManagedContainer()
    return container


class TestHandleManagedContainer:
    class TestGet:
        def test_returns_correct_object(self, container):
            object_in = MyObject()
            handle = container.add_object(object_in)
            object_out = container.get(handle)
            assert object_out == object_in

        def test_does_not_create_reference(self, container):
            object_in = MyObject()
            handle = container.add_object(object_in)
            object_out = container.get(handle)
            assert object_out == object_in
            expected_ref_count = 1
            actual_ref_count = sys.getrefcount(object_in) - 1
            assert expected_ref_count == actual_ref_count

        def test_returns_none_with_invalid_handle(self, container):
            handle = INVALID_HANDLE
            object_out = container.get(handle)
            assert object_out is None

        def test_returns_none_with_removed_handle(self, container):
            object_in = MyObject()
            handle = container.add_object(object_in)
            container.remove(handle)
            object_out = container.get(handle)
            assert object_out is None

        def test_handles_returns_none_with_cleared_container(self, container):
            object_in = MyObject()
            handle = container.add_object(object_in)
            container.clear()
            object_out = container.get(handle)
            assert object_out is None

    class TestRemove:
        def test_throws_handle_is_inactive_exception_with_already_removed_handle(self, container):
            object_in = MyObject()
            handle = container.add_object(object_in)
            container.remove(handle)
            with pytest.raises(HandleIsInactiveException):
                container.remove(handle)

    class TestAddObject:
        def test_does_not_create_reference(self, container):
            object_in = MyObject()
            container.add_object(object_in)
            expected_ref_count = 1
            actual_ref_count = sys.getrefcount(object_in) - 1
            assert expected_ref_count == actual_ref_count
