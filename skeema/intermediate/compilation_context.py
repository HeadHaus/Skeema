class CompilationContext:
    def __init__(self):
        self._representations = {}

    @property
    def representations(self):
        return self._representations.values()

    def register_representation(self, name, representation):
        self._representations[name] = representation

    def get_representation(self, name):
        return self._representations.get(name)

    def __str__(self):
        s = ''.join(str(representation) for representation in self.representations)
        return s
