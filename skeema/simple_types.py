import sys
from typing import TypeVar, List

T = TypeVar('T')


class Boolean:
    @classmethod
    def parse(cls, v):
        return Boolean(v)

    def __new__(cls, value=False):
        return bool(value)


class Integer(int):
    @classmethod
    def parse(cls, v):
        return Integer(v)


class Null:
    @classmethod
    def parse(cls, _v):
        return Null()


class Number(float):
    @classmethod
    def parse(cls, v):
        return Number(v)


class Object(tuple):
    @classmethod
    def parse(cls, v):
        return Object(**v)


class String(str):
    @classmethod
    def parse(cls, v):
        return String(v)


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
