from skeema.schema.schema_manager import SchemaManager as Base
from .schema import Schema


class SchemaManager(Base):
    def _create_schema(self, url, class_name, key_value_definition):
        return Schema(self, url, class_name, key_value_definition)
