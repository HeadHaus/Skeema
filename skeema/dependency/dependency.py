from abc import ABCMeta, abstractmethod
from skeema.dependency.dependency_node import DependencyNode


class DependencyHasNoNodeException(Exception):
    def __init__(self):
        msg = f"Dependency does not have a node. Was it added to a container?"
        super().__init__(msg)


class Dependency(metaclass=ABCMeta):
    def __init__(self):
        self._dependency_node = None

    def add_dependency(self, dependency):
        if self._dependency_node is None:
            raise DependencyHasNoNodeException()
        dependency_node = dependency.dependency_node
        self.dependency_node.add_dependency(dependency_node)

    @property
    def dependency_node(self):
        return self._dependency_node

    def on_add_to_container(self, handle, debug_name):
        self._dependency_node = DependencyNode(handle, debug_name)

    @abstractmethod
    def _find_dependencies(self):
        return NotImplementedError
