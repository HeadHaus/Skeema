import sys
import json
from inspect import signature

import skeema


def is_annotation_pod(annotation):
    pods = [
        'bool',
        'int',
        'float',
        'list',
        'str',
    ]
    return annotation in pods


class Parser:
    @staticmethod
    def class_lookup(module_name: str, class_name: str):
        module = sys.modules[module_name]
        return getattr(module, class_name)

    @staticmethod
    def parse(klass, json_instance):
        module_name = klass.__module__
        instance_def = json.loads(json_instance)
        init_signature = signature(klass)

        param_names = []
        klasses = []
        for parameter in init_signature.parameters.values():
            param_name = parameter.name
            param_names.append(param_name)
            annotation = parameter.annotation
            if is_annotation_pod(annotation):
                annotation_class = getattr(sys.modules['builtins'], annotation)
            else:
                annotation_class = Parser.class_lookup(module_name, annotation)
            klasses.append(annotation_class)
        param_name_klasses = zip(param_names, klasses)

        simple_types = [
            skeema.Boolean,
            skeema.Integer,
            skeema.Null,
            skeema.Number,
            skeema.String
        ]

        st_checks = [issubclass(klass, st) for st in simple_types]
        is_st = any(st_checks)
        if is_st:
            arg = instance_def
            return klass(arg)
        else:
            instances = {}
            for param_name, param_klass in param_name_klasses:
                arg = instance_def[param_name]
                instance = param_klass.parse(json.dumps(arg))
                instances[param_name] = instance
            return klass(**instances)
