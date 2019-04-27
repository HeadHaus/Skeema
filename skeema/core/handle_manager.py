from __future__ import annotations

from typing import TYPE_CHECKING

from .handle import Handle, INVALID_HANDLE
from .handle import (
    HandleInvalidException,
    HandleOutOfRangeException,
    HandleIsInactiveException,
    HandleIsRetiredException
)


class HandleEntry:
    def __init__(self) -> None:
        self.active: bool = False
        self.generation: int = 0


if TYPE_CHECKING:
    from typing import List
    HandleEntryList = List[HandleEntry]


class HandleManager:
    """
    Handle Manager
    """

    def __init__(self) -> None:
        self._num_active_handles: int = 0
        self._entries: HandleEntryList = list()

    @property
    def num_entries(self) -> int:
        return len(self._entries)

    @property
    def num_active_handles(self) -> int:
        return self._num_active_handles

    def issue_handle(self) -> Handle:
        """
        Issue a new handle for this manager.
        :return: The newly issued handle
        """

        index: int = self._num_active_handles
        # Grow entries list if necessary
        if len(self._entries) == index:
            handle_entry: HandleEntry = HandleEntry()
            self._entries.append(handle_entry)

        self._entries[index].active = True
        self._entries[index].generation += 1
        self._num_active_handles += 1
        handle: Handle = Handle(index, self._entries[index].generation)

        return handle

    def remove_handle(self, handle: Handle) -> None:
        """
        Removes control of the given handle from this manager.
        :param handle: The handle to be removed
        :return: None
        """

        self.validate_handle(handle)
        index: int = handle.index
        self._entries[index].active = False
        self._num_active_handles -= 1

    def remove_all_handles(self) -> None:
        """
        Removes control of all handles issued by this manager.
        :return: None
        """

        self._num_active_handles = 0
        for entry in self._entries:
            entry.active = False

    def validate_handle(self, handle: Handle) -> None:
        handle_is_valid: bool = handle != INVALID_HANDLE
        if not handle_is_valid:
            raise HandleInvalidException(self, handle)

        index: int = handle.index
        index_is_in_range: bool = index < self.num_entries
        if not index_is_in_range:
            raise HandleOutOfRangeException(self, handle)

        entry: HandleEntry = self._entries[index]
        handle_is_active: bool = entry.active
        if not handle_is_active:
            raise HandleIsInactiveException(self, handle)

        correct_generation: bool = entry.generation == handle.generation
        if not correct_generation:
            raise HandleIsRetiredException(self, handle, entry)
