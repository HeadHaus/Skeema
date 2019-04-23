import sys


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


simple_types = dict()
simple_types[Boolean.__name__.lower()] = Boolean
simple_types[Integer.__name__.lower()] = Integer
simple_types[Number.__name__.lower()] = Number
simple_types[Null.__name__.lower()] = Null
simple_types[Object.__name__.lower()] = Object
simple_types[String.__name__.lower()] = String

SKEEMA_MODULE = 'skeema'
module = sys.modules[SKEEMA_MODULE]

for t in simple_types.values():
    t.__module__ = module
    module.__dict__[t.__name__] = t
