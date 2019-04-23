class CircularDependencyException(Exception):
    def __init__(self, node_a, node_b):
        msg = f"A circular reference was detected between {node_a.debug_name} and {node_b.debug_name}."
        super().__init__(msg)


class DependencyGraph:
    """
    Dependency graph
    """

    def __init__(self, root_node):
        self._root_node = root_node

    def resolve_dependencies(self):
        resolved = []
        DependencyGraph.dependency_resolve(self._root_node, resolved)
        return resolved

    @staticmethod
    def dependency_resolve(node, resolved, _unresolved=()):
        unresolved = list(_unresolved)
        unresolved.append(node)
        for edge in node.dependency_nodes:
            if edge not in resolved:
                if edge in unresolved:
                    raise CircularDependencyException(node, edge)
                DependencyGraph.dependency_resolve(edge, resolved, unresolved)
        resolved.append(node)
        unresolved.remove(node)
