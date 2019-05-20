from __future__ import annotations

import sys
from inspect import Signature, Parameter, _POSITIONAL_OR_KEYWORD

from typing import TYPE_CHECKING

from skeema import util

if TYPE_CHECKING:
    pass


class ModelMeta(type):
    def __new__(mcs, class_name, class_parents, class_attrs, **kwargs):
        print(f'Creating class {class_name}')

        print(f"NAME: {class_name}")
        print(f"PARENTS: {class_parents}")
        print(f"ATTRS: {class_attrs}")
        print(f"KWARGS: {kwargs}")

        ModelMeta.build_attrs(class_attrs)

        class_attrs['parameters'] = kwargs['parameters'] if 'parameters' in kwargs else {}
        class_attrs['data_members'] = kwargs['data_members'] if 'data_members' in kwargs else {}

        return super().__new__(mcs, class_name, class_parents, class_attrs)

    def __init__(cls, class_name, class_parents, class_attrs, **kwargs):
        print(f'Initializing class {class_name}')
        super().__init__(class_name, class_parents, class_attrs)

        cls.supers = class_parents

        # Instance property; can only be set once cls is created by `new`
        cls.klass = cls

        if 'parameters' in kwargs.keys():
            parameters = kwargs['parameters']
            annotation_dict = {
                name: annotation
                for name, annotation in parameters.items()
            }
            cls.__annotations__ = annotation_dict

    @property
    def annotations(cls):
        return cls.__annotations__

    def annotation(cls, name):
        return cls.annotations[name]

    @property
    def signature(cls):
        return cls.__signature__

    @property
    def __signature__(cls):
        parameters = [
            Parameter(name, annotation=annotation, kind=_POSITIONAL_OR_KEYWORD)
            for name, annotation in cls.__annotations__.items()
        ]
        _signature = Signature(parameters=parameters, return_annotation=None)
        return _signature

    @staticmethod
    def build_attrs(class_attrs):
        # INSTANCE METHODS
        def __init__(self, *args, **kwargs):
            print(f'initializing object of type {self.klass}: {args}, {kwargs}')

            # Super arguments
            # If there is no data members for an argument, the data member exists in the super class
            #
            super_parameters = dict([
                item for item in self.klass.parameters.items() if item not in self.klass.data_members.items()
            ])
            super_arguments = {}
            # Positional arguments
            super_arguments.update({name: value for name, value in zip(super_parameters.keys(), args)})
            # Keyword arguments
            super_arguments.update({name: value for name, value in kwargs.items() if name in super_parameters.keys()})
            super_klass = self.klass.supers[0] if len(self.klass.supers) > 0 else None
            if super_klass is not None:
                super(self.klass, self).__init__(**super_arguments)

            # Non super arguments
            # If there is a data member for an argument, it is managed by this class
            #
            parameters = dict([
                item for item in self.klass.parameters.items() if item in self.klass.data_members.items()
            ])
            arguments = {}
            # Positional arguments
            arguments.update({name: value for name, value in zip(parameters.keys(), args)})
            # Keyword arguments
            arguments.update({name: value for name, value in kwargs.items() if name in parameters.keys()})
            for name, value in arguments.items():
                self.set_attribute(name, value)

        if '__init__' not in class_attrs:
            class_attrs['__init__'] = __init__

        def get_attribute(self, name):
            if name == 'value':
                print(f'GETTING ATTR {name}')
                attr = object.__getattribute__(self, name)
            else:
                attr = object.__getattribute__(self, name)
            return attr

        class_attrs['__getattribute__'] = get_attribute
        class_attrs['get_attribute'] = get_attribute

        def set_attribute(self, name, value):
            print(f'SETTING ATTR {name}: {value}')
            annotation = self.klass.annotation(name)
            if util.is_annotation_pod(annotation):
                annotation_class = getattr(sys.modules['builtins'], annotation)
                if type(value) is annotation_class:
                    object.__setattr__(self, name, value)
                else:
                    raise TypeError
            elif util.is_annotation_array(annotation):
                if type(value) is list:
                    object.__setattr__(self, name, value)
                else:
                    raise TypeError
            else:
                annotation_klass = util.class_lookup(self.__module__, annotation)
                if hasattr(annotation_klass, 'type_check') and annotation_klass.type_check(value):
                    object.__setattr__(self, name, value)
                else:
                    raise TypeError

        class_attrs['__setattr__'] = set_attribute
        class_attrs['set_attribute'] = set_attribute


class Array(metaclass=ModelMeta):
    value: list

    def __init__(self, value: list):
        self.value = value

    def __eq__(self, other):
        return self.value == other

    def __iter__(self):
        return iter(self.value)


class Boolean(metaclass=ModelMeta):
    @classmethod
    def type_check(cls, value):
        ty = type(value)
        if ty is bool or cls in ty.__mro__:
            return True
        else:
            return False

    value: bool

    def __init__(self, value: bool):
        self.value = value

    def __bool__(self):
        return self.value

    def __eq__(self, other: Boolean):
        return self.value == other


class Integer(metaclass=ModelMeta):
    @classmethod
    def type_check(cls, value):
        ty = type(value)
        if ty is int or cls in ty.__mro__:
            return True
        else:
            return False

    value: int

    def __init__(self, value: int):
        self.value = value

    def __eq__(self, other):
        return self.value == other


class Null:
    pass


class Number(metaclass=ModelMeta):
    @classmethod
    def type_check(cls, value):
        ty = type(value)
        if ty is float or cls in ty.__mro__:
            return True
        else:
            return False

    value: float

    def __init__(self, value: float):
        self.value = value

    def __eq__(self, other):
        return self.value == other


class Object(metaclass=ModelMeta):
    @classmethod
    def type_check(cls, _value):
        return True

    def __init__(self):
        pass


class String(metaclass=ModelMeta):
    @classmethod
    def type_check(cls, value):
        ty = type(value)
        if ty is str or cls in ty.__mro__:
            return True
        else:
            return False

    value: str

    def __init__(self, value: str):
        self.value = value

    def __eq__(self, other):
        return self.value == other


simple_types = [
    Array,
    Boolean,
    Integer,
    Null,
    Number,
    Object,
    String
]

SKEEMA_MODULE = 'skeema'
module = sys.modules[SKEEMA_MODULE]

for t in simple_types:
    t.__module__ = module
    module.__dict__[t.__name__] = t
