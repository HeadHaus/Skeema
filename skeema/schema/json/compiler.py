from .keyword import *
from skeema.schema.compiler import Compiler as Base


class Compiler(Base):
    def get_compilation_keys(self):
        compilation_keys = list()
        compilation_keys.append(Type())
        compilation_keys.append(Properties())
        compilation_keys.append(AllOf())
        compilation_keys.append(Required())
        return compilation_keys
