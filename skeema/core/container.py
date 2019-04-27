from skeema.core.handle import INVALID_HANDLE
from skeema.core.proxy_container import ProxyContainer


class Container:
    """
    Container
    """

    def __init__(self):
        # Storage for object references added to the container to preserve their lifetimes
        self._objects = []
        self._proxy_container = ProxyContainer()

        # Mapping of ids to handles
        self._id_to_object_handle_map = dict()

    def add_object(self, obj_id, obj, obj_debug_name):
        # Do not add duplicate resources
        if obj_id in self._id_to_object_handle_map:
            return INVALID_HANDLE
        handle = self._proxy_container.add_object(obj)
        obj.on_add_to_container(handle, obj_debug_name)
        self._id_to_object_handle_map[obj_id] = handle
        self._objects.append(obj)
        return handle

    def get_object_handle(self, obj_id):
        if obj_id in self._id_to_object_handle_map:
            return self._id_to_object_handle_map[obj_id]
        else:
            return INVALID_HANDLE

    def get_object(self, handle):
        resource = self._proxy_container.get(handle)
        return resource

    def clear(self):
        self._objects.clear()
        self._proxy_container.clear()
        self._id_to_object_handle_map.clear()
