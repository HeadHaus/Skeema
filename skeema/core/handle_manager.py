from .handle import Handle, INVALID_HANDLE
from .handle import HandleInvalidException, HandleOutOfRangeException, HandleIsInactiveException, HandleIsRetiredException


class HandleManager:
    """
    Handle Manager
    """

    class HandleEntry:
        def __init__(self):
            self.active = False
            self.generation = 0

    def __init__(self):
        self._active_handles = 0
        self._entries = []

    @property
    def active_handles(self):
        return self._active_handles

    def issue_handle(self):
        index = self._active_handles
        # Grow entries list
        if len(self._entries) == index:
            handle_entry = HandleManager.HandleEntry()
            self._entries.append(handle_entry)
        self._entries[index].active = True
        self._entries[index].generation += 1
        self._active_handles += 1
        handle = Handle(index, self._entries[index].generation)
        return handle

    def remove_handle(self, handle):
        if self.validate_handle(handle):
            index = handle.index
            self._entries[index].active = False
            self._active_handles -= 1

    def remove_all_handles(self):
        """
        Invalidates all handles issued by this manager.
        """
        self._active_handles = 0
        for entry in self._entries:
            entry.active = False

    def validate_handle(self, handle):
        handle_is_valid = handle != INVALID_HANDLE
        if not handle_is_valid:
            raise HandleInvalidException(self, handle)

        index = handle.index
        index_is_in_range = index < len(self._entries)
        if not index_is_in_range:
            raise HandleOutOfRangeException(self, handle)

        entry = self._entries[index]
        handle_is_active = entry.active
        if not handle_is_active:
            raise HandleIsInactiveException(self, handle)

        correct_generation = entry.generation == handle.generation
        if not correct_generation:
            raise HandleIsRetiredException(self, handle, entry)

        if (not handle_is_valid
            or not index_is_in_range
            or not correct_generation
            or not handle_is_active):
            return False
        return True
