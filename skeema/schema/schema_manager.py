from __future__ import annotations

from typing import TYPE_CHECKING
from abc import abstractmethod, ABCMeta

from skeema.core.container import Container
from skeema.core.handle import INVALID_HANDLE

if TYPE_CHECKING:
    from skeema.core.handle import Handle
    from skeema.types import KeyValueDef

    from .schema import Schema


class SchemaManager(metaclass=ABCMeta):
    def __init__(self) -> None:
        self._container = Container()

    def create_schema(self, url: str, class_name: str, key_value_definition: KeyValueDef) -> Schema:
        if self.get_schema_handle(url) is not INVALID_HANDLE:
            schema = self.get_schema(url)
            return schema
        else:
            schema = self._create_schema(url, class_name, key_value_definition)
            self.add_schema(schema)
            return schema

    @abstractmethod
    def _create_schema(self, url: str, class_name: str, key_value_definition: KeyValueDef) -> Schema:
        pass

    def add_schema(self, schema: Schema) -> Handle:
        handle = self._container.add_object(schema.url, schema, schema.url)
        return handle

    def get_schema_handle(self, url: str) -> Handle:
        return self._container.get_object_handle(url)

    def get_schema_from_handle(self, handle: Handle):
        return self._container.get_object(handle)

    def get_schema(self, url: str) -> Schema:
        handle = self.get_schema_handle(url)
        schema = self.get_schema_from_handle(handle)
        return schema
