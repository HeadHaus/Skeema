from __future__ import annotations

from abc import abstractmethod, ABCMeta
from urllib.parse import urlparse, urljoin
from typing import TYPE_CHECKING

from skeema.core import Compilable

from .compiler import Compiler

if TYPE_CHECKING:
    from typing import Dict

    from skeema.types import KeyValueDef
    from skeema.intermediate import CompilationContext

    from .schema_manager import SchemaManager

    PropertyNameToClassMap = Dict[str, str]


class Schema(Compilable, metaclass=ABCMeta):
    @property
    @abstractmethod
    def compiler(self) -> Compiler:
        pass

    """
    Schema data
    """
    def __init__(self, manager: SchemaManager, url: str, class_name: str, key_value_definition: KeyValueDef) -> None:
        super().__init__()

        # SchemaManager
        self._manager = manager

        # The url used to identify this schema using references, i.e. $ref
        # Because urls are inherently unique, they also act as the key for schema manager
        self._url = url

        # The class name defined by the schema
        self._class_name = class_name

        # The internal json stored as a KeyValueDefinition
        self._key_value_definition = key_value_definition

        # Mapping of properties to class names - used during compilation
        self._property_map = dict()

    @property
    def key_value_definition(self) -> KeyValueDef:
        return self._key_value_definition

    @property
    def url(self) -> str:
        return self._url

    @property
    def class_name(self) -> str:
        return self._class_name

    @property
    def property_map(self) -> PropertyNameToClassMap:
        return self._property_map

    def _resolve_dependency_url(self, dependency_url_string: str) -> str:
        dependency_url = urlparse(dependency_url_string)
        if dependency_url.netloc:
            return dependency_url_string

        # TODO
        # Right now we assume the dependency is defined relative to this one.

        return urljoin(self._url, dependency_url_string)

    @abstractmethod
    def _populate_dependency_node(self) -> None:
        pass

    def _compile(self, compilation_context: CompilationContext) -> None:
        self._populate_dependency_node()

        child_dependency_nodes = self.dependency_node.resolve_dependencies()[:-1]
        for child_dependency_node in child_dependency_nodes:
            handle = child_dependency_node.handle
            dependency = self._manager.get_schema_from_handle(handle)
            dependency.compile(compilation_context)

        self.compiler.compile(self, compilation_context)
