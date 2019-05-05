import pytest
import json

from skeema.schema.json import SchemaManager
from skeema.intermediate.compiler.compiler import Compiler


@pytest.fixture(name='compiler')
def create_compiler():
    return Compiler()


@pytest.fixture(name='manager')
def create_manager():
    return SchemaManager()


def test_parser(manager, compiler):
    person_def = {
        "type": "object",
        "properties": {
            "firstName": {"type": "string"},
            "lastName": {"type": "string"},
            "age": {"type": "integer"}
        }
    }
    manager.create_schema('schemas/person.json', 'Person', person_def)

    address_def = {
        "type": "object",
        "properties": {
            "addressLine1": {"type": "string"},
            "addressLine2": {"type": "string"},
            "city": {"type": "string"},
            "province": {"type": "string"},
            "postalCode": {"type": "string"},
            "owner": {"$ref": "./person.json"}
        }
    }
    manager.create_schema('schemas/address.json', 'Address', address_def)

    schema = manager.get_schema('schemas/address.json')
    context = schema.compile()
    compiler.compile(context)

    from skeema import Address, Person

    person_v = {
        'firstName': 'Robert',
        'lastName': 'Dempsey',
        'age': 34
    }
    address_v = {
        'addressLine1': '1804  Ontario St',
        'addressLine2': 'Apt 4',
        'postalCode': 'L2N 1S8',
        'city': 'St Catharines',
        'province': 'ON',
        'owner': person_v
    }

    json_str = json.dumps(address_v)

    addr = Address.parse(json_str)
    assert addr.addressLine1 == '1804  Ontario St'
    assert addr.addressLine2 == 'Apt 4'
    assert addr.postalCode == 'L2N 1S8'
    assert addr.city == 'St Catharines'
    assert addr.province == 'ON'

    owner = addr.owner
    assert owner.firstName == 'Robert'
    assert owner.lastName == 'Dempsey'
    assert owner.age == 34
