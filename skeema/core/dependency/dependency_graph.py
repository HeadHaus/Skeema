from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .dependency_node import DependencyNode, DependencyNodeList


class CircularDependencyException(Exception):
    def __init__(self, node_a: DependencyNode, node_b: DependencyNode):
        msg = f"A circular reference was detected between {node_a.debug_name} and {node_b.debug_name}."
        super().__init__(msg)


class DependencyGraph:
    """
    Dependency graph
    """

    def __init__(self, root_node: DependencyNode) -> None:
        self._root_node = root_node

    def resolve_dependencies(self) -> DependencyNodeList:
        resolved = []
        DependencyGraph.dependency_resolve(self._root_node, resolved)
        return resolved

    @staticmethod
    def dependency_resolve(node: DependencyNode, resolved: DependencyNodeList, unresolved: DependencyNodeList = None):
        if unresolved is None:
            unresolved = []

        unresolved.append(node)

        for dependency in node.dependency_nodes:
            if dependency not in resolved:
                if dependency in unresolved:
                    raise CircularDependencyException(node, dependency)
                DependencyGraph.dependency_resolve(dependency, resolved, unresolved)

        resolved.append(node)
        unresolved.remove(node)
