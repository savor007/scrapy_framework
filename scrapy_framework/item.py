class Item(object):
    """
    框架内的item对象
    """
    def __init__(self, data):
        self._item=data


    @property
    def data(self):
        return self._item