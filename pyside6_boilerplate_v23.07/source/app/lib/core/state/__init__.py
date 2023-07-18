from lib.helper import MetaSingleton

class AbstractState(metaclass=MetaSingleton):
    def __init__(self):
        self.data = {}
        self.updateMethods = {}
        self.partialUpdateMethods = {}

    def use(self, key, init_value=[]):
        self.data[key] = init_value
        self.updateMethods[key] = {}
        self.partialUpdateMethods[key] = [{} for _ in init_value]

    def use_QItemModel(self, key, init_value=[]):
        self.use(key, init_value)
        for i in range(len(self.data[key])):
            self.data[key][i].dataChanged.connect(
                lambda:self._update(key,i))

    def use_customModel(self, key, init_value=[]):
        self.use(key, init_value)
        for i in range(len(self.data[key])):
            self.data[key][i].bind_data(
                lambda v:self._update(key,i))

    def set(self, key, value, index=None):
        if index == None:
            self.data[key] = value
            self._update(key)
        else:
            self.data[key][index] = value
            self._update(key, index)

    def setPartial(self, key, index, value):
        self.set(key, value, index)


    def get(self, key, index=None):
        if index == None:
            return self.data[key]
        else:
            return self.data[key][index]

    def append(self, key, value, index):
        self.data[key].append(index, value)
        self.partialUpdateMethods[key].append(index, {})
        self._update(key)

    def insert(self, key, value, index):
        self.data[key].insert(index, value)
        self.partialUpdateMethods[key].insert(index, {})
        self._update(key)

    def delete(self, key, index):
        del self.data[key][index]
        del self.partialUpdateMethods[key][index]
        self._update(key)

    def bind(self, key, method, index=None):
        fid = id(method)
        if index == None:
            self.updateMethods[key][fid] = method
        else:
            self.partialUpdateMethods[key][index][fid] = method
        self._update(key, index)
    
    def _update(self, key, index=None):
        if index == None:
            method_keys = list(self.updateMethods[key].keys())
            for fid in method_keys:
                try:
                    method = self.updateMethods[key][fid]
                    method(self.data[key])
                except RuntimeError:
                    del self.updateMethods[key][fid]
            for i, methods in enumerate(self.partialUpdateMethods[key]):
                method_keys = list(methods.keys())
                for fid in method_keys:
                    try:
                        method = methods[fid]
                        method(self.data[key][i])
                    except RuntimeError:
                        del self.partialUpdateMethods[key][i][fid]
        else:
            method_keys = list(self.partialUpdateMethods[key][index].keys())
            for fid in method_keys:
                try:
                    method = self.partialUpdateMethods[key][index][fid]
                    method(self.data[key][index])
                except RuntimeError:
                    del self.partialUpdateMethods[key][index][fid]