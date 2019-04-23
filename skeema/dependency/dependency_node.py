from .dependency_graph import DependencyGraph


class DependencyNode:
    def __init__(self, handle, debug_name):
        self._handle = handle
        self._debug_name = debug_name
        self._dependency_nodes = []
        self._graph = DependencyGraph(self)

    @property
    def debug_name(self):
        return self._debug_name

    @property
    def handle(self):
        return self._handle

    @property
    def dependency_nodes(self):
        return self._dependency_nodes

    def add_dependency(self, node):
        self._dependency_nodes.append(node)
        # Resolve dependencies iteratively to catch any circular dependencies
        self._graph.resolve_dependencies()

    def resolve_dependencies(self):
        return self._graph.resolve_dependencies()