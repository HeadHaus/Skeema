from .class_builder import ClassBuilder


class Compiler:
    def compile(self, context):
        representations = context.representations
        for r in representations:
            class_name = r.class_name
            base_classes = r.base_classes
            parameters = r.parameters
            data_members = r.data_members
            ClassBuilder.create_class(class_name, base_classes, parameters, data_members)
