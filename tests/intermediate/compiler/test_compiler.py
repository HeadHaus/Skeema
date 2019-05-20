import pytest
from inspect import signature, Parameter, _ParameterKind

from skeema.schema.json import SchemaManager
from skeema.intermediate.compiler.compiler import Compiler


@pytest.fixture(name='compiler')
def create_compiler():
    return Compiler()


@pytest.fixture(name='manager')
def create_manager():
    return SchemaManager()


class TestCompiler:
    class TestCompile:
        def test_creates_class_from_boolean(self, compiler, manager):
            json = {"type": "boolean"}
            schema = manager.create_schema('schemas/boolean.json', 'TestBoolean', json)
            context = schema.compile()
            compiler.compile(context)

            from skeema import TestBoolean
            parameters = list(signature(TestBoolean).parameters.values())
            expected_parameters = [Parameter('value', kind=_ParameterKind.POSITIONAL_OR_KEYWORD, annotation='bool')]
            assert parameters == expected_parameters

            b = TestBoolean(False)
            assert b == False
            b = TestBoolean(True)
            assert b == True

        def test_creates_class_from_integer(self, compiler, manager):
            json = {"type": "integer"}
            schema = manager.create_schema('schemas/integer.json', 'TestInteger', json)
            context = schema.compile()
            compiler.compile(context)

            from skeema import TestInteger
            parameters = list(signature(TestInteger).parameters.values())
            expected_parameters = [Parameter('value', kind=_ParameterKind.POSITIONAL_OR_KEYWORD, annotation='int')]
            assert parameters == expected_parameters

            i = TestInteger(124)
            assert i == 124

        # TODO: What does a null object type mean?
        # def test_creates_class_from_null(self, compiler, manager):
        #     json = {"type": "null"}
        #     schema = manager.create_schema('schemas/null.json', 'TestNull', json)
        #     context = schema.compile()
        #     compiler.compile(context)
        #
        #     from skeema import TestNull
        #     parameters = list(signature(TestNull).parameters.values())
        #     assert parameters == []

        def test_creates_class_from_number(self, compiler, manager):
            json = {"type": "number"}
            schema = manager.create_schema('schemas/number.json', 'TestNumber', json)
            context = schema.compile()
            compiler.compile(context)

            from skeema import TestNumber

            parameters = list(signature(TestNumber).parameters.values())
            expected_parameters = [Parameter('value', kind=_ParameterKind.POSITIONAL_OR_KEYWORD, annotation='float')]
            assert parameters == expected_parameters

            n = TestNumber(3.141592653)
            assert n == 3.141592653

        def test_creates_class_from_string(self, compiler, manager):
            json = {"type": "string"}
            schema = manager.create_schema('schemas/string.json', 'TestString', json)
            context = schema.compile()
            compiler.compile(context)

            from skeema import TestString

            parameters = list(signature(TestString).parameters.values())
            expected_parameters = [Parameter('value', kind=_ParameterKind.POSITIONAL_OR_KEYWORD, annotation='str')]
            assert parameters == expected_parameters

            s = TestString('Hello, world!')
            assert s == 'Hello, world!'

        def test_creates_class_from_array(self, compiler, manager):
            json = {
                'type': 'array',
                'items': {
                    'type': 'integer'
                }
            }
            schema = manager.create_schema('schemas/array.json', 'TestArray', json)
            context = schema.compile()
            compiler.compile(context)

            from skeema import TestArray

            parameters = list(signature(TestArray).parameters.values())
            expected_parameters = [Parameter('value', kind=_ParameterKind.POSITIONAL_OR_KEYWORD, annotation='[int]')]
            assert parameters == expected_parameters

            s = TestArray([0, 1, 2])
            assert s == [0, 1, 2]

            for i, v in enumerate(s):
                assert i == v

            s = TestArray([0, 1, 2])
            i = iter(s)
            assert next(i) == 0
            assert next(i) == 1
            assert next(i) == 2

        def test_creates_class_from_object(self, compiler, manager):
            json = {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "age": {"type": "integer"},
                    "married": {"type": "boolean"}
                }
            }
            schema = manager.create_schema('schemas/object.json', 'Person', json)
            context = schema.compile()
            compiler.compile(context)

            from skeema import Person

            parameters = list(signature(Person).parameters.values())
            expected_parameters = [
                Parameter('name', kind=_ParameterKind.POSITIONAL_OR_KEYWORD, annotation='NameClass'),
                Parameter('age', kind=_ParameterKind.POSITIONAL_OR_KEYWORD, annotation='AgeClass'),
                Parameter('married', kind=_ParameterKind.POSITIONAL_OR_KEYWORD, annotation='MarriedClass')
            ]
            assert parameters == expected_parameters

            person = Person(name='Brandon', age=26, married=False)
            assert person.name == 'Brandon'
            assert person.age == 26
            assert person.married == False

        def test_creates_class_from_object_with_references(self, compiler, manager):
            person_kv = {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "age": {"type": "integer"},
                    "married": {"type": "boolean"}
                }
            }

            book_kv = {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "author": {"$ref": "./person.json"}
                }
            }

            manager.create_schema('schemas/person.json', 'Person', person_kv)
            manager.create_schema('schemas/book.json', 'Book', book_kv)
            schema = manager.get_schema('schemas/book.json')
            context = schema.compile()
            compiler.compile(context)

            from skeema import Person, Book

            parameters = list(signature(Book).parameters.values())
            expected_parameters = [
                Parameter('title', kind=_ParameterKind.POSITIONAL_OR_KEYWORD, annotation='TitleClass'),
                Parameter('author', kind=_ParameterKind.POSITIONAL_OR_KEYWORD, annotation='Person')
            ]
            assert parameters == expected_parameters

            person = Person('J.K. Rowling', 26, False)
            book = Book('Harry Potter', person)
            assert book.title == 'Harry Potter'
            assert book.author == person

        def test_creates_classes_from_object_definitions(self, compiler, manager):
            person_kv = {
                "definitions": {
                    "address": {
                        "type": "object",
                        "properties": {
                            "address_line_1": {"type": "string"},
                            "address_line_2": {"type": "string"},
                            "city": {"type": "string"},
                            "province": {"type": "string"},
                        }
                    }
                },
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "address": {"$ref": "#/definitions/address"}
                }
            }

            schema = manager.create_schema('schemas/person.json', 'Person', person_kv)
            context = schema.compile()
            compiler.compile(context)

            from skeema import Address, Person

            parameters = list(signature(Address).parameters.values())
            expected_parameters = [
                Parameter('address_line_1', kind=_ParameterKind.POSITIONAL_OR_KEYWORD, annotation='AddressLine1Class'),
                Parameter('address_line_2', kind=_ParameterKind.POSITIONAL_OR_KEYWORD, annotation='AddressLine2Class'),
                Parameter('city', kind=_ParameterKind.POSITIONAL_OR_KEYWORD, annotation='CityClass'),
                Parameter('province', kind=_ParameterKind.POSITIONAL_OR_KEYWORD, annotation='ProvinceClass')
            ]
            assert parameters == expected_parameters

            parameters = list(signature(Person).parameters.values())
            expected_parameters = [
                Parameter('name', kind=_ParameterKind.POSITIONAL_OR_KEYWORD, annotation='NameClass'),
                Parameter('address', kind=_ParameterKind.POSITIONAL_OR_KEYWORD, annotation='Address')
            ]
            assert parameters == expected_parameters

            address = Address('50 Rideau Street', 'Suite 100', 'Ottawa', 'ON')
            assert address.address_line_1 == '50 Rideau Street'
            assert address.address_line_2 == 'Suite 100'
            assert address.city == 'Ottawa'
            assert address.province == 'ON'
            person = Person('Phillip Sherman', address)
            assert person.name == 'Phillip Sherman'
            assert person.address == address
