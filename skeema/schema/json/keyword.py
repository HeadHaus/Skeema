from abc import abstractmethod, ABCMeta

from skeema.intermediate.parameter import Parameter
from skeema.intermediate.data_member import DataMember
from skeema.util import to_camel_case


class Keyword(metaclass=ABCMeta):
    def __init__(self):
        self.data = None
        self.error_message = None

    @property
    @abstractmethod
    def key(self):
        pass

    def compile(self, schema, class_context, compilation_context):
        self._precompile(schema)
        if self.data:
            compiled = self._compile(schema, class_context, compilation_context)
            return compiled
        else:
            return False

    def _precompile(self, schema):
        data = schema.key_value_definition
        if self.key in data:
            self.data = data[self.key]

    @abstractmethod
    def _compile(self, schema, class_context, compilation_context):
        pass


class Type(Keyword):
    @property
    def key(self):
        return "type"

    def _compile(self, schema, class_context, compilation_context):
        class_type = self.data
        class_context.class_type = class_type

        if class_type is 'object' or class_type is 'null':
            return True

        is_array = False
        if class_type is 'array':
            is_array = True
            items = schema.key_value_definition['items']
            if type(items) is dict:
                class_type = items['type']
            else:
                self.error_message = 'Invalid array type'
                return False

        klass = to_camel_case(class_type)

        # Do not extend the klass type if the object is an array
        if is_array:
            class_context.base_classes.append('Array')
        else:
            class_context.base_classes.append(klass)

        data_member_values = dict()
        data_member_values['name'] = "value"
        data_member_values['klass'] = klass
        data_member_values['array'] = is_array
        data_member = DataMember(**data_member_values)
        class_context.add_data_member(data_member)

        constructor_parameter_values = dict()
        constructor_parameter_values['name'] = "value"
        constructor_parameter_values['klass'] = klass
        constructor_parameter_values['data_member'] = data_member
        constructor_parameter_values['required'] = False
        constructor_parameter_values['array'] = is_array
        parameter = Parameter(**constructor_parameter_values)
        class_context.add_constructor_parameter(parameter)

        return True


class Properties(Keyword):
    @property
    def key(self):
        return "properties"

    def _compile(self, schema, class_context, compilation_context):
        if class_context.class_type is None:
            self.error_message = f"Schemas defining properties must be of type 'object'. " \
                                 f"No type found."
            return False

        if class_context.class_type != 'object':
            self.error_message = f"Schemas defining properties must be of type 'object'. " \
                                 f"Found type {class_context.class_type}."
            return False

        properties = self.data

        for property_name in properties:
            data_member_values = dict()
            data_member_values['name'] = property_name
            data_member_values['klass'] = None

            constructor_parameter_values = dict()
            constructor_parameter_values['name'] = property_name
            constructor_parameter_values['klass'] = None
            constructor_parameter_values['required'] = False
            constructor_parameter_values['array'] = False

            property = properties[property_name]

            if "$ref" in property:
                reference = property["$ref"]
                dependency_url = schema._resolve_dependency_url(reference)
                dependency = schema._manager.get_schema(dependency_url)
                assert dependency.compiled is True
                type_name = dependency.class_name
                data_member_values['klass'] = type_name
                constructor_parameter_values['klass'] = type_name

            elif "type" in property:
                type_name = schema.property_map[property_name]
                data_member_values['klass'] = type_name
                constructor_parameter_values['klass'] = type_name

            elif "allOf" in property:
                # TODO
                # type must be object. Do we throw an assert here?
                type_name = schema.property_map[property_name]
                data_member_values['klass'] = type_name
                constructor_parameter_values['klass'] = type_name

            else:
                continue

            data_member = DataMember(**data_member_values)
            class_context.add_data_member(data_member)

            constructor_parameter_values['data_member'] = data_member
            constructor_parameter = Parameter(**constructor_parameter_values)
            class_context.add_constructor_parameter(constructor_parameter)

        return True


class AllOf(Keyword):
    def __init__(self):
        super().__init__()

    @property
    def key(self):
        return "allOf"

    def _compile(self, schema, class_context, compilation_context):
        all_of = self.data

        return True


class Required(Keyword):
    def __init__(self):
        super().__init__()

    @property
    def key(self):
        return "required"

    def _compile(self, schema, class_context, compilation_context):
        required = self.data

        constructor_parameters = class_context.constructor_parameters

        for parameter in constructor_parameters:
            if parameter.name in required:
                parameter.required = True

        return True
