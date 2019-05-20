import pytest

from skeema.intermediate.representation import Representation
from skeema.intermediate.parameter import Parameter
from skeema.intermediate.data_member import DataMember
from skeema.schema.json import SchemaManager


@pytest.fixture(autouse=True, name='manager')
def manager():
    return SchemaManager()


class TestJsonSchema:
    class TestCompile:
        def test_creates_the_expected_representation_with_root_type_boolean(self, manager):
            kv = {
                "type": "boolean"
            }
            schema = manager.create_schema('schemas/test/test.json', 'Test', kv)
            context = schema.compile()
            representation = context.get_representation('Test')
            data_members = []
            parameters = [Parameter('value', 'bool', None, True, False)]
            expected_representation = Representation('Test', ['Boolean'], parameters, data_members)
            assert representation == expected_representation

        def test_creates_the_expected_representation_with_root_type_integer(self, manager):
            kv = {
                "type": "integer"
            }
            schema = manager.create_schema('schemas/test/test.json', 'Test', kv)
            context = schema.compile()
            representation = context.get_representation('Test')
            data_members = []
            parameters = [Parameter('value', 'int', None, True, False)]
            expected_representation = Representation('Test', ['Integer'], parameters, data_members)
            assert representation == expected_representation

        def test_creates_the_expected_representation_with_root_type_null(self, manager):
            kv = {
                "type": "null"
            }
            schema = manager.create_schema('schemas/test/test.json', 'Test', kv)
            context = schema.compile()
            representation = context.get_representation('Test')
            expected_representation = Representation('Test', [], [], [])
            assert representation == expected_representation

        def test_creates_the_expected_representation_with_root_type_number(self, manager):
            kv = {
                "type": "number"
            }
            schema = manager.create_schema('schemas/test/test.json', 'Test', kv)
            context = schema.compile()
            representation = context.get_representation('Test')
            data_members = []
            parameters = [Parameter('value', 'float', None, True, False)]
            expected_representation = Representation('Test', ['Number'], parameters, data_members)
            assert representation == expected_representation

        def test_creates_the_expected_representation_with_root_type_object(self, manager):
            kv = {
                "type": "object"
            }
            schema = manager.create_schema('schemas/test/test.json', 'Test', kv)
            context = schema.compile()
            representation = context.get_representation('Test')
            data_members = []
            parameters = []
            expected_representation = Representation('Test', ['Object'], parameters, data_members)
            assert representation == expected_representation

        def test_creates_the_expected_representation_with_root_type_object_and_properties(self, manager):
            kv = {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "age": {"type": "string"},
                    "gender": {"type": "string"}
                }
            }
            schema = manager.create_schema('schemas/test/test.json', 'Test', kv)
            context = schema.compile()
            representation = context.get_representation('Test')
            data_members = [
                DataMember('name', 'NameClass'),
                DataMember('age', 'AgeClass'),
                DataMember('gender', 'GenderClass')
            ]
            parameters = [
                Parameter('name', 'NameClass', data_members[0]),
                Parameter('age', 'AgeClass', data_members[1]),
                Parameter('gender', 'GenderClass', data_members[2])
            ]
            expected_representation = Representation('Test', ['Object'], parameters, data_members)
            assert representation == expected_representation

        def test_creates_the_expected_representation_with_root_type_string(self, manager):
            kv = {
                "type": "string"
            }
            schema = manager.create_schema('schemas/test/test.json', 'Test', kv)
            context = schema.compile()
            representation = context.get_representation('Test')
            data_members = []
            parameters = [Parameter('value', 'str', None, True, False)]
            expected_representation = Representation('Test', ['String'], parameters, data_members)
            assert representation == expected_representation

        def test_creates_the_expected_representation_with_root_type_array(self, manager):
            kv = {
                "type": "array",
                "items": {
                    "type": "number"
                }
            }
            schema = manager.create_schema('schemas/test/test.json', 'Test', kv)
            context = schema.compile()
            representation = context.get_representation('Test')
            data_members = []
            parameters = [Parameter('value', 'float', None, True, True)]
            expected_representation = Representation('Test', ['Array'], parameters, data_members)
            assert representation == expected_representation

        def test_creates_representations_for_each_property(self, manager):
            kv = {
                "type": "object",
                "properties": {
                    "name":		{"type": "string"},
                    "age":  	{"type": "string"},
                    "gender":	{"type": "string"}
                }
            }
            schema = manager.create_schema('schemas/v1/person.json', 'Person', kv)
            context = schema.compile()
            assert len(context.representations) == 4
            assert context.get_representation('Person') is not None
            assert context.get_representation('NameClass') is not None
            assert context.get_representation('AgeClass') is not None
            assert context.get_representation('GenderClass') is not None

        def test_creates_a_representation_with_a_parameter_and_data_member_for_each_property(self, manager):
            kv = {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "age": {"type": "string"},
                    "gender": {"type": "string"}
                }
            }
            schema = manager.create_schema('schemas/v1/person.json', 'Person', kv)
            context = schema.compile()
            person = context.get_representation('Person')
            assert len(person.parameters) == 3
            assert len(person.data_members) == 3

        def test_creates_a_representation_with_a_parameter_and_data_member_for_each_reference_property(self, manager):
            person_kv = {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "age": {"type": "string"},
                    "gender": {"type": "string"}
                }
            }
            book_kv = {
                "type": "object",
                "properties": {
                    "author": {"$ref": "./person.json"}
                }
            }
            manager.create_schema('schemas/test/person.json', 'Person', person_kv)
            manager.create_schema('schemas/test/book.json', 'Book', book_kv)

            context = manager.get_schema('schemas/test/book.json').compile()
            book = context.get_representation('Book')
            assert book.parameters[0] == Parameter('author', 'Person', DataMember('author', 'Person')).json
            assert book.data_members[0] == DataMember('author', 'Person').json
