from abc import abstractmethod, ABCMeta
from skeema.core.dependency import Dependency
from skeema.intermediate import CompilationContext


class Compilable(Dependency, metaclass=ABCMeta):
    """
    Interface for compilable class.

    Compilation should be done in the following order:

        1) Populate the dependency graph in order:

                The subclass must define a method for determining any other compilable resources this resource is
                dependent on. Each time we add a dependency, we insert it into the instance's dependency graph. The
                dependency graph will determine the order in which the dependencies must be compiled, and catches any
                circular dependencies.

        2) Compile all dependencies in the dependency graph:

                All dependencies must be compiled prior to compiling this resource. We traverse the ordered list of
                dependencies determined by the dependency graph, and compile them in order by calling the subclass's
                compile() method.

                This resource will be also be compiled during this time, after all of its dependencies have been
                compiled. It will always be the last resource in the ordered dependency graph.
    """

    def __init__(self) -> None:
        super().__init__()
        self._compiled: bool = False

    @property
    def compiled(self) -> bool:
        return self._compiled

    def _precompile(self, compilation_context: CompilationContext) -> None:
        pass

    @abstractmethod
    def _compile(self, compilation_context: CompilationContext) -> None:
        pass

    def compile(self, compilation_context: CompilationContext = None) -> CompilationContext:
        if compilation_context is None:
            compilation_context = CompilationContext()

        if self.compiled is True:
            return compilation_context

        self._precompile(compilation_context)
        self._compile(compilation_context)
        self._compiled = True

        return compilation_context
