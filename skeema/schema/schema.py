from urllib.parse import urlparse, urljoin
from abc import abstractmethod, ABCMeta

from skeema.core.compilable import Compilable


class Schema(Compilable, metaclass=ABCMeta):
    @property
    @abstractmethod
    def compiler(self):
        pass

    """
    Schema data
    """
    def __init__(self, manager, url, class_name, key_value_definition):
        super().__init__()

        # SchemaManager
        self._manager = manager

        # The url used to identify this schema using references, i.e. $ref
        # Because urls are inherently unique, they also act as the key for schema manager
        self._url = url

        # The class name defined by the schema
        self._class_name = class_name

        # The internal json stored as a dict
        self._key_value_definition = key_value_definition

        # Mapping of properties to class names - used during compilation
        self._property_map = dict()

    @property
    def key_value_definition(self):
        return self._key_value_definition

    @property
    def url(self):
        return self._url

    @property
    def class_name(self):
        return self._class_name

    @property
    def property_map(self):
        return self._property_map

    def _resolve_dependency_url(self, dependency_url_string):
        dependency_url = urlparse(dependency_url_string)
        if dependency_url.netloc:
            return dependency_url_string

        # TODO
        # Right now we assume the dependency is defined relative to this one.

        return urljoin(self._url, dependency_url_string)

    @abstractmethod
    def _populate_dependency_node(self):
        pass

    def _compile(self, compilation_context):
        self._populate_dependency_node()

        child_dependency_nodes = self.dependency_node.resolve_dependencies()[:-1]
        for child_dependency_node in child_dependency_nodes:
            handle = child_dependency_node.handle
            dependency = self._manager.get_schema_from_handle(handle)
            dependency.compile(compilation_context)

        self.compiler.compile(self, compilation_context)

    @staticmethod
    def search_definition(indict, filter_key):
        if isinstance(indict, dict):
            for key, value in indict.items():
                if filter_key == key:
                    yield value
                # Parse dict
                elif isinstance(value, dict):
                    for d in Schema.search_definition(value, filter_key):
                        yield d
                # Parse list
                elif isinstance(value, list) or isinstance(value, tuple):
                    for v in value:
                        for d in Schema.search_definition(v, filter_key):
                            yield d
