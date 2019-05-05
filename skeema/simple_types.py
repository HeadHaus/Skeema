import sys


class Boolean:
    def __init__(self, value):
        self._value = value

    def __bool__(self):
        return bool(self._value)

    def __eq__(self, other):
        return bool(self._value) == other


class Integer(int):
    pass


class Null:
    pass


class Number(float):
    pass


class Object(tuple):
    pass


class String(str):
    pass


simple_types = [
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
