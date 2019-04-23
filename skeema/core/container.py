from skeema.core.handle import INVALID_HANDLE
from skeema.core.handle_managed_container import HandleManagedContainer


class Container:
    """
    Container
    """

    def __init__(self):
        # Storage for object references added to the container to preserve their lifetimes
        self._objects = []
        self._object_handle_manager = HandleManagedContainer()

        # Mapping of ids to handles
        self._id_to_object_handle_map = dict()

    def add_object(self, obj_id, obj, obj_debug_name):
        # Do not add duplicate resources
        if obj_id in self._id_to_object_handle_map:
            return INVALID_HANDLE
        handle = self._object_handle_manager.add_object(obj)
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
        resource = self._object_handle_manager.get(handle)
        return resource

    def clear(self):
        self._objects.clear()
        self._object_handle_manager.clear()
        self._id_to_object_handle_map.clear()
