from __future__ import annotations

from abc import ABCMeta

from .dependency_node import DependencyNode
from ..handle import Handle


class DependencyHasNoNodeException(Exception):
    def __init__(self) -> None:
        msg = f"Dependency does not have a node. Was it added to a container?"
        super().__init__(msg)


class Dependency(metaclass=ABCMeta):
    def __init__(self) -> None:
        self._dependency_node = None

    def add_dependency(self, dependency: Dependency) -> None:
        if self._dependency_node is None:
            raise DependencyHasNoNodeException()
        dependency_node = dependency.dependency_node
        self.dependency_node.add_dependency(dependency_node)

    @property
    def dependency_node(self) -> DependencyNode:
        return self._dependency_node

    def on_add_to_container(self, handle: Handle, debug_name: str) -> None:
        self._dependency_node = DependencyNode(handle, debug_name)
