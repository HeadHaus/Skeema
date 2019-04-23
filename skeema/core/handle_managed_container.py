from weakref import proxy

from .handle import HandleValidationException
from .handle_manager import HandleManager


class HandleManagedContainer:
    """
    Handle Managed Container
    """

    def __init__(self):
        self._handle_manager = HandleManager()
        self._object_proxies = []

    def add_object(self, obj):
        handle = self._handle_manager.issue_handle()
        # Grow object proxies list if needed
        if len(self._object_proxies) == handle.index:
            self._object_proxies.append(None)
        self._object_proxies[handle.index] = proxy(obj)
        return handle

    def get(self, handle):
        try:
            self._handle_manager.validate_handle(handle)
        except HandleValidationException:
            return None
        return self._object_proxies[handle.index]

    def remove(self, handle):
        self._object_proxies[handle.index] = None
        self._handle_manager.remove_handle(handle)

    def clear(self):
        self._handle_manager.remove_all_handles()
        self._object_proxies.clear()
