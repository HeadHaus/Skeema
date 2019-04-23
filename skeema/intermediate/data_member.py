class DataMember:
    def __init__(self, name, klass):
        self._name = name
        self._klass = klass

    @property
    def name(self):
        return self._name

    @property
    def klass(self):
        return self._klass

    @property
    def json(self):
        return {
            'name': self.name,
            'class': self.klass,
        }
