class ClassContext:
    def __init__(self, class_name):
        self._class_name = class_name
        # The class meta type as defined by the schema
        self._class_type = None
        self._base_classes = []
        self._constructor_parameters = []
        self._data_members = []

    @property
    def class_name(self):
        return self._class_name

    @property
    def class_type(self):
        return self._class_type

    @class_type.setter
    def class_type(self, class_type):
        self._class_type = class_type

    @property
    def base_classes(self):
        return self._base_classes

    @property
    def constructor_parameters(self):
        return self._constructor_parameters

    @property
    def data_members(self):
        return self._data_members

    def add_constructor_parameter(self, parameter):
        self._constructor_parameters.append(parameter)

    def add_data_member(self, member):
        self._data_members.append(member)
