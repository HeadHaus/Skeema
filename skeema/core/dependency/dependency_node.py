from __future__ import annotations

from typing import TYPE_CHECKING, List

from .dependency_graph import DependencyGraph

if TYPE_CHECKING:
    from ..handle import Handle


class DependencyNode:
    def __init__(self, handle: Handle, debug_name: str) -> None:
        self._handle = handle
        self._debug_name = debug_name
        self._dependency_nodes = []
        self._graph = DependencyGraph(self)

    @property
    def handle(self) -> Handle:
        return self._handle

    @property
    def debug_name(self) -> str:
        return self._debug_name

    @property
    def dependency_nodes(self) -> DependencyNodeList:
        return self._dependency_nodes

    def add_dependency(self, node: DependencyNode) -> None:
        self._dependency_nodes.append(node)
        # Resolve dependencies iteratively to catch any circular dependencies
        self._graph.resolve_dependencies()

    def resolve_dependencies(self) -> DependencyNodeList:
        return self._graph.resolve_dependencies()


DependencyNodeList = List[DependencyNode]
