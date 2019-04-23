import pytest

from skeema.dependency.dependency import Dependency, DependencyHasNoNodeException
from skeema.dependency.dependency_graph import CircularDependencyException
from skeema.core.container import Container


@pytest.fixture(name="container")
def create_container():
    container = Container()
    return container


class MyDependency(Dependency):
    def _find_dependencies(self):
        pass


def create_dependency(container, _id):
    dependency = MyDependency()
    container.add_object(_id, dependency, _id)
    return dependency


class TestDependency:
    class TestAddDependency:
        def test_throws_dependency_has_no_node_exception_with_dependency_without_node(self):
            d0 = MyDependency()
            d1 = MyDependency()

            with pytest.raises(DependencyHasNoNodeException):
                d1.add_dependency(d0)

        def test_throws_circular_dependency_exception_with_simple_circular_reference(self, container, id0, id1):
            d0 = create_dependency(container, id0)
            d1 = create_dependency(container, id1)

            with pytest.raises(CircularDependencyException):
                d0.add_dependency(d1)
                d1.add_dependency(d0)

        def test_throws_circular_dependency_exception_with_complex_circular_reference(self, container, id0, id1, id2, id3, id4):
            d0 = create_dependency(container, id0)
            d1 = create_dependency(container, id1)
            d2 = create_dependency(container, id2)
            d3 = create_dependency(container, id3)
            d4 = create_dependency(container, id4)

            with pytest.raises(CircularDependencyException):
                d4.add_dependency(d3)
                d3.add_dependency(d2)
                d2.add_dependency(d1)
                d1.add_dependency(d0)
                d0.add_dependency(d4)

        def test_throws_circular_dependency_exception_with_self_as_dependency(self, container, id0):
            d0 = create_dependency(container, id0)

            with pytest.raises(CircularDependencyException):
                d0.add_dependency(d0)

    class TestResolveDependencies:
        def test_returns_a_list_of_the_graph_dependency_nodes_in_the_correct_order(self, container, id0, id1, id2, id3, id4):
            d0 = create_dependency(container, id0)
            d1 = create_dependency(container, id1)
            d2 = create_dependency(container, id2)
            d3 = create_dependency(container, id3)
            d4 = create_dependency(container, id4)

            #   d0
            #   |
            #   d1
            #  / \
            # d2 d3
            #  \ /
            #  d4
            #
            # d4: d0, d1, d2, d3, d4

            d4.add_dependency(d2)
            d4.add_dependency(d3)
            d2.add_dependency(d1)
            d3.add_dependency(d1)
            d1.add_dependency(d0)

            dependency_nodes = d4.dependency_node.resolve_dependencies()
            expected_dependency_nodes = [
                d0.dependency_node,
                d1.dependency_node,
                d2.dependency_node,
                d3.dependency_node,
                d4.dependency_node
            ]

            assert dependency_nodes == expected_dependency_nodes
