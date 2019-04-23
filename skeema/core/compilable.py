from abc import abstractmethod, ABCMeta
from skeema.dependency.dependency import Dependency
from skeema.intermediate.compilation_context import CompilationContext


class Compilable(Dependency, metaclass=ABCMeta):
    """
    Interface for compilable class

    Compilation should be done in the following order:
        1) Determine dependencies from subclass:
                The subclass must define a method for determining any other compilable resources this resource is
                dependent on. At this stage, we simply want to build an unordered list of dependencies.

        2) Create dependency graph:
                Here, we analyze the dependencies and determine the order in which we must compile them.

        3) Compile all dependencies in the dependency graph in order:
                All dependencies must be compiled prior to compiling this resource. We traverse the list of dependencies
                and compile them in order by calling the subclass's compile() method.
                This resource will be also be compiled during this time, after all of its dependencies have been
                compiled. It will always be the last resource in the ordered dependency graph.

    """

    def __init__(self):
        super().__init__()
        self._compiled = False

    @property
    def compiled(self):
        return self._compiled

    def _precompile(self, compilation_context):
        pass

    @abstractmethod
    def _compile(self, compilation_context):
        pass

    def compile(self, compilation_context=None):
        if compilation_context is None:
            compilation_context = CompilationContext()
        if self.compiled is True:
            return compilation_context
        self._precompile(compilation_context)
        self._compile(compilation_context)
        self._compiled = True
        return compilation_context
