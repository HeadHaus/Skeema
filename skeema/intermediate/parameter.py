class Parameter:
    def __init__(self, name: str, klass: str, data_member, required=True, array=False):
        self._name = name
        self._klass = klass
        self._data_member = data_member
        self._required = required
        self._array = array

    def __eq__(self, other):
        return True if \
            self.name == other.name and \
            self.json == other.json \
            else False

    @property
    def name(self):
        return self._name

    @property
    def klass(self):
        return self._klass

    @property
    def required(self):
        return self._required

    @property
    def data_member(self):
        return self._data_member

    @property
    def array(self):
        return self._array

    @required.setter
    def required(self, value):
        self._required = value

    @property
    def json(self):
        return {
            'name': self.name,
            'class': self.klass,
            'data_member': self.data_member.name
        }
