from urllib.parse import urljoin

from skeema.schema.schema import Schema as Base

from .compiler import Compiler


class Schema(Base):
    _compiler = Compiler()

    @property
    def compiler(self):
        return Schema._compiler

    @property
    def definitions(self):
        return self.key_value_definition.get("definitions")

    @property
    def properties(self):
        return self.key_value_definition.get("properties")

    def _find_dependencies(self):
        dependencies = [ref for ref in Schema.search_definition(self.key_value_definition, "$ref")]
        return dependencies

    def _precompile(self, compilation_context):
        self._create_definition_schemas()

    def _create_definition_schemas(self):
        # Create schemas out of the inline class definitions.
        # Inline class schemas do not count as referenced dependencies until an explicit $ref is made.
        raw_schema = {}
        if self.definitions is not None:
            raw_schema = self.definitions
        for inline_class_name in raw_schema:
            inline_class_definition = raw_schema[inline_class_name]
            url = urljoin(self.url, f"#/definitions/{inline_class_name}")
            self._manager.create_schema(url, inline_class_name.capitalize(), inline_class_definition)

    def _populate_dependency_node(self):
        dependency_keywords = (
            "properties",
            "$ref",
            "allOf",
            "anyOf",
            "oneOf"
        )

        filtered_keywords = [k for k in self.key_value_definition.keys() if k in dependency_keywords]
        num_filtered_keywords = len(filtered_keywords)
        if num_filtered_keywords == 0:
            return
        if num_filtered_keywords > 1:
            assert f"Schema {self.class_name} must only define 1 top level keyword, but currently defines " \
                f"{num_filtered_keywords}: {filtered_keywords}."

        keyword = filtered_keywords[0]

        if keyword == "properties":
            raw_schema = self.properties
            for property_name in raw_schema:
                property_definition = raw_schema[property_name]

                if "$ref" in property_definition:
                    reference_url = property_definition["$ref"]
                    dependency_url = self._resolve_dependency_url(reference_url)
                    schema = self._manager.get_schema(dependency_url)
                    class_name = schema.class_name
                else:
                    class_name = f"{property_name.capitalize()}Class"
                    url = f"{self._url}#/properties/{class_name}"
                    schema = self._manager.create_schema(url, class_name, property_definition)

                self.add_dependency(schema)

                # Since the "properties" object is the only place that defines named class members (properties), we
                # should take this opportunity to create a class definition where we map property names to class names.
                # This way, we can look up the class name from the property name during compilation.

                # Why do we check here for instances of "allOf" within a property?
                # Instead of mapping the property to an anonymous class that contains only the "allOf" definition and
                # no properties, it is more useful to the user to map the property to the final combined class that is
                # assembled from the list of classes defined in the "allOf" definition.
                if "allOf" in property_definition:
                    self._property_map[property_name] = f"{class_name}_allOf"
                else:
                    self._property_map[property_name] = class_name

        elif keyword == "$ref":
            reference_url = self._key_value_definition["$ref"]
            dependency_url = self._resolve_dependency_url(reference_url)
            dependency = self._manager.get_schema(dependency_url)
            self.add_dependency(dependency)

        elif keyword == "allOf":
            raw_schema_list = self._key_value_definition["allOf"]

            # Create a combined schema definition
            combined_class_definition = dict()
            combined_class_definition["type"] = "object"
            combined_class_definition["properties"] = dict()

            for raw_schema in raw_schema_list:
                # Retrieve the properties from the referenced schema
                if "$ref" in raw_schema:
                    # Find the schema in the manager
                    reference_url = raw_schema["$ref"]
                    dependency_url = self._resolve_dependency_url(reference_url)
                    dependency = self._manager.get_schema(dependency_url)
                    # Update the combined class with the schema properties
                    property_names = dependency.properties
                    combined_class_definition["properties"].update(property_names)

                # Take the raw property definition
                else:
                    property_names = raw_schema["properties"]
                    combined_class_definition["properties"].update(property_names)

            # Create a combined schema from the definition
            combined_class_name = f"{self.class_name}_allOf"
            url = self._url
            schema = self._manager.create_schema(url, combined_class_name, combined_class_definition)
            self.add_dependency(schema)
