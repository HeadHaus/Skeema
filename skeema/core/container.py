from __future__ import annotations

from typing import TYPE_CHECKING

from skeema.core.handle import INVALID_HANDLE
from skeema.core.proxy_container import ProxyContainer

if TYPE_CHECKING:
    from typing import Any, Dict

    from skeema.core import Handle

    IdToHandleMap = Dict[str, Handle]


class Container:
    """
    Container
    """

    def __init__(self) -> None:
        # Storage for object references added to the container to preserve their lifetimes
        self._objects: [Any] = []
        self._proxy_container: ProxyContainer = ProxyContainer()

        # Mapping of ids to handles
        self._id_to_object_handle_map: IdToHandleMap = {}

    def add_object(self, obj_id: str, obj: Any, obj_debug_name: str) -> Handle:
        # Do not add duplicate resources
        if obj_id in self._id_to_object_handle_map:
            return INVALID_HANDLE

        handle: Handle = self._proxy_container.add_object(obj)
        obj.on_add_to_container(handle, obj_debug_name)
        self._id_to_object_handle_map[obj_id] = handle
        self._objects.append(obj)

        return handle

    def get_object_handle(self, obj_id: str) -> Handle:
        if obj_id in self._id_to_object_handle_map:
            return self._id_to_object_handle_map[obj_id]
        else:
            return INVALID_HANDLE

    def get_object(self, handle: Handle) -> Any:
        resource: Any = self._proxy_container.get(handle)
        return resource

    def clear(self) -> None:
        self._objects.clear()
        self._proxy_container.clear()
        self._id_to_object_handle_map.clear()
