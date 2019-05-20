from __future__ import annotations

import sys

from skeema.intermediate.compiler.parser import Parser
from skeema import ModelMeta
from skeema import util


def private(name):
    return f'_{name}'


class ClassBuilder:
    """
    ClassBuilder
    """

    @staticmethod
    def set_class_module(klass, module_name: str):
        klass.__module__ = module_name
        module = sys.modules[module_name]
        module.__dict__[klass.__name__] = klass

    @staticmethod
    def create_class(class_name: str, base_classes: [str], parameters: [dict], data_members: [dict]):
        module_name = 'skeema'

        # Populate a dictionary of property accessors
        cls_dict = dict()

        # Parsing for json
        def parse(cls, json_str: str):
            return Parser.parse(cls, json_str)
        cls_dict['parse'] = classmethod(parse)

        def decorate(annotation: str, array: bool) -> str:
            if array:
                return f'[{annotation}]'
            else:
                return annotation

        parameter_annotation_dict = {
            name: decorate(annotation, array) for name, annotation, array in
            ((parameter['name'], parameter['class'], parameter['array']) for parameter in parameters)
        }

        data_member_dict = {
            name: decorate(annotation, array) for name, annotation, array in
            ((data_member['name'], data_member['class'], data_member['array']) for data_member in data_members)
        }

        cls = ModelMeta(
            class_name,
            tuple(util.class_lookup(module_name, base_class) for base_class in base_classes),
            cls_dict,
            parameters=parameter_annotation_dict,
            data_members=data_member_dict
        )

        ClassBuilder.set_class_module(cls, module_name)

        return cls
