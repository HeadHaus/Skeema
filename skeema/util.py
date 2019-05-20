import sys
import re


def to_camel_case(snake):
    components = snake.split('_')
    components = (c.replace(c[0], c[0].upper(), 1) for c in components)
    return ''.join(components)


def is_annotation_pod(annotation):
    pods = [
        'bool',
        'int',
        'float',
        'list',
        'str',
    ]
    return annotation in pods


def is_annotation_array(annotation):
    regex = r'\[...\]'
    result = re.match(regex, annotation)
    return result is not None


def class_lookup(module_name: str, class_name: str):
    _module = sys.modules[module_name]
    if hasattr(_module, class_name):
        return getattr(_module, class_name)
    else:
        return None
