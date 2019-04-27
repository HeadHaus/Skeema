from typing import Any
from weakref import proxy

from .handle import Handle, HandleValidationException
from .handle_manager import HandleManager


class ProxyContainer:
    """
    Handle Managed Container
    """

    def __init__(self) -> None:
        self._handle_manager = HandleManager()
        self._object_proxies = []

    def add_object(self, obj: Any) -> Handle:
        handle = self._handle_manager.issue_handle()
        # Grow object proxies list if needed
        if len(self._object_proxies) == handle.index:
            self._object_proxies.append(None)
        self._object_proxies[handle.index] = proxy(obj)
        return handle

    def get(self, handle: Handle) -> proxy:
        try:
            self._handle_manager.validate_handle(handle)
        except HandleValidationException:
            return None
        return self._object_proxies[handle.index]

    def remove(self, handle: Handle) -> None:
        self._object_proxies[handle.index] = None
        self._handle_manager.remove_handle(handle)

    def clear(self) -> None:
        self._handle_manager.remove_all_handles()
        self._object_proxies.clear()
