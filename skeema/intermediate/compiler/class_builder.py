from __future__ import annotations

import sys
from types import FunctionType

from .operator import itemgetter, itemsetter
from .node import *
from skeema import Boolean
from skeema.intermediate import DataMember, Parameter
from skeema.intermediate.compiler.parser import Parser


def private(name):
    return f'_{name}'


class ClassBuilder:
    """
    ClassBuilder
    """

    @staticmethod
    def compile_function(function_node: FunctionNode):
        flags = annotations.compiler_flag
        function_code = compile(
            function_node(),
            '<skeema>',
            'exec',
            flags=flags
        )

        signature_node = function_node.signature_node
        num_parameters = len(signature_node.parameters) - 1
        index = num_parameters + 1
        function = FunctionType(function_code.co_consts[index], globals(), function_node.name)
        function.__annotations__ = signature_node.as_dict()

        return function

    @staticmethod
    def set_class_module(klass, module_name: str):
        klass.__module__ = module_name
        module = sys.modules[module_name]
        module.__dict__[klass.__name__] = klass

    @staticmethod
    def class_lookup(module_name: str, class_name: str):
        module = sys.modules[module_name]
        return getattr(module, class_name)

    @staticmethod
    def create_class(class_name: str, base_classes: [str], parameters: [Parameter], data_members: [DataMember]):
        module_name = 'skeema'

        # Populate a dictionary of property accessors
        cls_dict = dict()

        def getitem(self, key: str):
            data_member_name = private(key)
            return self.__dict__[data_member_name]

        # Enables use of itemgetter
        cls_dict['__getitem__'] = getitem

        data_member_class_map = {
            data_member['name']: ClassBuilder.class_lookup(module_name, data_member['class'])
            for data_member in data_members
        }

        def setitem(self, key: str, value: any):
            value_klass = type(value)
            expected_klass = data_member_class_map[key]

            def check_type(_value_klass, _expected_klass):
                # The value is valid if its class is part of the expected class hierarchy
                # e.g., str is part of the String hierarchy
                valid = _value_klass in _expected_klass.__mro__
                # The value is valid if it is a bool, and the expected class is part of the Boolean hierarchy
                valid = valid or (_value_klass is bool and issubclass(_expected_klass, Boolean))
                if not valid:
                    raise TypeError(
                        f'Invalid type for {key} = {value}: expected type {_expected_klass}, received type {_value_klass}')

            if value_klass is list:
                for item in value:
                    item_klass = type(item)
                    check_type(item_klass, expected_klass)
            else:
                check_type(value_klass, expected_klass)
                if value_klass is not expected_klass:
                    # The value class is a sub or supertype.
                    # Cast value to expected class
                    value = expected_klass(value)

            data_member_name = private(key)
            self.__dict__[data_member_name] = value

        # Enables use of itemsetter
        cls_dict['__setitem__'] = setitem

        cls_dict.update({
            name: property(
                itemgetter(name),
                itemsetter(name)
            ) for name in (data_member['name'] for data_member in data_members)
        })

        parameter_nodes = [
            ParameterNode(
                parameter['name'],
                parameter['class'],
                parameter['array']
            ) for parameter in parameters]
        parameter_list_nodes = ParameterListNode(parameter_nodes)
        signature_node = SignatureNode('__init__', parameter_list_nodes)

        assignment_nodes = [
            AssignmentNode(
                ValueNode(f'self.{data_member}'),
                ValueNode(value)
            ) for data_member, value in [(parameter['data_member'], parameter['name']) for parameter in parameters]
        ]

        init_node = MethodNode(signature_node, assignment_nodes)
        init = ClassBuilder.compile_function(init_node)
        cls_dict['__init__'] = init

        # Parsing for json
        def parse(cls, json_str):
            return Parser.parse(cls, json_str)
        cls_dict['parse'] = classmethod(parse)

        cls = type(
            class_name,
            tuple(ClassBuilder.class_lookup(module_name, base_class) for base_class in base_classes),
            cls_dict
        )

        ClassBuilder.set_class_module(cls, module_name)

        return cls
