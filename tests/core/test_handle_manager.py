import pytest

from skeema.core.handle import Handle, INVALID_HANDLE
from skeema.core.handle import HandleInvalidException, HandleOutOfRangeException, HandleIsInactiveException, HandleIsRetiredException
from skeema.core.handle_manager import HandleManager


@pytest.fixture(name="manager")
def create_handle_manager():
    handle_manager = HandleManager()
    return handle_manager


class TestHandleManager:
    def test_manager_starts_with_no_active_handles(self, manager):
        assert manager.num_active_handles == 0

    class TestIssueHandle:
        def test_returns_new_handle(self, manager):
            handle = manager.issue_handle()
            assert handle.generation == 1
            assert handle.index == 0

        def test_returns_valid_handle(self, manager):
            handle = manager.issue_handle()
            manager.validate_handle(handle)

        def test_increments_active_count(self, manager):
            active_handles = manager.num_active_handles
            manager.issue_handle()
            assert manager.num_active_handles == active_handles + 1

    class TestRemoveHandle:
        @pytest.fixture(name="handle")
        def issue_handle(self, manager):
            handle = manager.issue_handle()
            return handle

        def test_decrements_active_count(self, manager, handle):
            active_handles = manager.num_active_handles
            manager.remove_handle(handle)
            assert manager.num_active_handles == active_handles - 1

        def test_throws_handle_is_inactive_exception_with_already_removed_handle(self, manager, handle):
            manager.remove_handle(handle)
            with pytest.raises(HandleIsInactiveException):
                manager.remove_handle(handle)

    class TestValidate:
        def test_throws_invalid_handle_exception_with_orphan_handle(self, manager):
            handle = Handle()
            with pytest.raises(HandleInvalidException):
                manager.validate_handle(handle)

        def test_throws_invalid_handle_exception_with_invalid_handle(self, manager):
            handle = INVALID_HANDLE
            with pytest.raises(HandleInvalidException):
                manager.validate_handle(handle)

        def test_handle_throws_handle_out_of_range_exception_with_stranger_handle(self, manager):
            stranger_manager = HandleManager()
            handle = stranger_manager.issue_handle()
            with pytest.raises(HandleOutOfRangeException):
                manager.validate_handle(handle)

        def test_throws_handle_is_inactive_exception_with_inactive_handle(self, manager):
            handle = manager.issue_handle()
            manager.remove_handle(handle)
            with pytest.raises(HandleIsInactiveException):
                manager.validate_handle(handle)

        def test_validate_retired_handle_throws_handle_is_retired_exception(self, manager):
            handle = manager.issue_handle()
            manager.remove_handle(handle)
            manager.issue_handle()
            with pytest.raises(HandleIsRetiredException):
                manager.validate_handle(handle)

    class TestRemoveAllHandles:
        def test_deactivates_issued_handles(self, manager):
            handle1 = manager.issue_handle()
            handle2 = manager.issue_handle()
            handle3 = manager.issue_handle()
            manager.remove_all_handles()
            with pytest.raises(HandleIsInactiveException):
                manager.validate_handle(handle1)
            with pytest.raises(HandleIsInactiveException):
                manager.validate_handle(handle2)
            with pytest.raises(HandleIsInactiveException):
                manager.validate_handle(handle3)
