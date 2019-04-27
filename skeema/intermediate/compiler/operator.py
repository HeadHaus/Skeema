class itemgetter:
    def __init__(self, item):
        self._item = item

        def func(obj):
            return obj[item]

        self._call = func

    def __call__(self, obj):
        return self._call(obj)


class itemsetter:
    def __init__(self, item):
        self._item = item

        def func(obj, value):
            obj[item] = value

        self._call = func

    def __call__(self, obj, value):
        self._call(obj, value)
