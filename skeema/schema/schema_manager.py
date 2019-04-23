from abc import abstractmethod, ABCMeta

from skeema.core.container import Container
from skeema.core.handle import INVALID_HANDLE


class SchemaManager(metaclass=ABCMeta):
    def __init__(self):
        self._container = Container()

    def create_schema(self, url, class_name, key_value_definition):
        assert type(url) == str

        if self.get_schema_handle(url) is not INVALID_HANDLE:
            schema = self.get_schema(url)
            return schema

        schema = self._create_schema(url, class_name, key_value_definition)
        self.add_schema(schema)
        return schema

    @abstractmethod
    def _create_schema(self, url, class_name, key_value_definition):
        pass

    def add_schema(self, schema):
        # print("\tAdding schema:", schema.class_name)
        handle = self._container.add_object(schema.url, schema, schema.url)
        return handle

    def get_schema_handle(self, url):
        return self._container.get_object_handle(url)

    def get_schema_from_handle(self, handle):
        return self._container.get_object(handle)

    def get_schema(self, url):
        handle = self.get_schema_handle(url)
        schema = self.get_schema_from_handle(handle)
        return schema
