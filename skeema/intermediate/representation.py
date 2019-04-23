import json


class Representation:
    def __init__(self, class_name, base_classes, parameters, data_members):
        self._class_name = class_name
        self._base_classes = base_classes
        self._parameters = parameters
        self._data_members = data_members

    def __eq__(self, other):
        return True if \
            self.class_name == other.class_name and \
            self.json == other.json \
            else False

    @property
    def class_name(self):
        return self._class_name

    @property
    def base_classes(self):
        return self._base_classes

    @property
    def parameters(self):
        return [parameter.json for parameter in self._parameters]

    @property
    def data_members(self):
        return [member.json for member in self._data_members]

    @property
    def json(self):
        obj = {
            "className": self.class_name,
            "baseClasses": json.dumps(self.base_classes),
            "parameters": self.parameters,
            "dataMembers": self.data_members
        }
        return obj

    def __str__(self):
        return str(self.json)
