class DataMember:
    def __init__(self, name, klass, array=False):
        self._name = name
        self._klass = klass
        self._array = array

    @property
    def name(self):
        return self._name

    @property
    def klass(self):
        return self._klass

    @property
    def array(self):
        return self._array

    @property
    def json(self):
        return {
            'name': self.name,
            'class': self.klass,
            'array': self.array
        }
