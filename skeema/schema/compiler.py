from abc import abstractmethod, ABCMeta

from skeema.intermediate import ClassContext, Representation


class Compiler(metaclass=ABCMeta):
    @abstractmethod
    def get_compilation_keys(self):
        pass

    def compile(self, schema, compilation_context):
        class_name = schema.class_name
        class_context = ClassContext(class_name)
        compilation_keys = self.get_compilation_keys()
        compiled_keys = dict()
        for compilation_key in compilation_keys:
            compiled = compilation_key.compile(schema, class_context, compilation_context)
            if compiled:
                compiled_keys[compilation_key.key] = compilation_key
            else:
                if compilation_key.error_message is not None:
                    print(
                        f"Warning during schema compilation for {schema.class_name} - "
                        f"compilation key \"{compilation_key.key}\" failed to compile:\n"
                        f"{compilation_key.error_message}")

        constructor_parameters = class_context.constructor_parameters
        data_members = class_context.data_members
        representation = Representation(class_name, class_context.base_classes, constructor_parameters, data_members)
        compilation_context.register_representation(class_name, representation)
