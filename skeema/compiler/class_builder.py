import sys
from types import FunctionType

from .operator import itemgetter, itemsetter
from .node import *
from skeema import Boolean
from skeema.intermediate.parameter import Parameter
from skeema.intermediate.data_member import DataMember


def private(name):
    return f'_{name}'


class ClassBuilder:
    """
    ClassBuilder
    """

    @staticmethod
    def create_method(method_name: str, signature_node: SignatureNode, body_nodes: [Node]):
        method_node = MethodNode(signature_node, body_nodes)
        method_code = compile(
            method_node(),
            '<skeema>',
            'exec'
        )

        index = 1
        if not body_nodes:
            index = 0

        init_function = FunctionType(method_code.co_consts[index], globals(), method_name)

        return init_function

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
            data_member['name']: ClassBuilder.class_lookup(module_name, data_member['class']) for data_member in data_members
        }

        def setitem(self, key: str, value: any):
            value_klass = type(value)
            expected_klass = data_member_class_map[key]

            # The value is valid if its class is part of the expected class hierarchy
            # e.g., str is part of the String hierarchy
            valid = value_klass in expected_klass.__mro__
            # The value is valid if it is a bool, and the expected class is part of the Boolean hierarchy
            valid = valid or (value_klass is bool and issubclass(expected_klass, Boolean))
            if not valid:
                raise TypeError(f'Invalid type for {key} = {value}: expected type {expected_klass}, received type {value_klass}')

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
                parameter['class']
            ) for parameter in parameters]
        parameter_list_nodes = ParameterListNode(parameter_nodes)
        signature_node = SignatureNode('init', parameter_list_nodes)

        assignment_pairs = [(parameter['name'], parameter['data_member']) for parameter in parameters]
        assignment_nodes = [
            AssignmentNode(
                ValueNode(f'self.{data_member}'),
                ValueNode(value)
            ) for data_member, value in [(p[0], p[1]) for p in assignment_pairs]
        ]

        init = ClassBuilder.create_method('init', signature_node, assignment_nodes)
        cls_dict['__init__'] = init

        cls = type(
            class_name,
            tuple(ClassBuilder.class_lookup(module_name, base_class) for base_class in base_classes),
            cls_dict
        )

        ClassBuilder.set_class_module(cls, module_name)

        return cls
