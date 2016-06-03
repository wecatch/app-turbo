import functools
import inspect
import weakref
import os

_mutation = {}

def register(state):
    def outwrapper(func):
        state.register(func)
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper
    return outwrapper


class CallFuncAsAttr(object):

    class __CallObject(object):

        def __init__(self, func):
            self.func = func

        def __call__(self, *args, **kwargs):
            return self.func(*args, **kwargs)

    def __init__(self, file_attr):
        name = file_attr
        filepath = os.path.abspath(file_attr)
        if os.path.isfile(filepath):
            name, ext = os.path.splitext(os.path.basename(filepath))

        setattr(self, self._name, {})
        _mutation[name] = weakref.ref(self)

    @property
    def __get_func(self):
        return getattr(self, self._name)      

    def register(self, func):
        if not inspect.isfunction(func):
            raise TypeError("argument expect function, now is '%s'"%func)

        name = func.func_name
        if name == (lambda x:x).func_name:
            raise TypeError('lambda is not allowed')

        self.__get_func[name] = self.__CallObject(func)

    def __getattr__(self, name):
        if name not in self.__get_func:
            raise AttributeError("%s object has no attribute '%s'"%(self.__class__.__name__, name))

        return self.__get_func[name]


class State(object):
    
    _state = {}

    def __init__(self):
        self.__set_state()

    def __set_state(self):
        State._state[self._name] = {}

    def __setattr__(self, name, value):
        State._state[self._name][name] = value

    def __getattr__(self, name):
        if name not in State._state[self._name]:
            raise AttributeError("%s object has no attribute '%s'"%(self.__class__.__name__, name))

        return State._state[self._name][name]

    @property
    def _name(self):
        return 'state_%s'%id(self)


class Mutation(CallFuncAsAttr):
    
    @property
    def _name(self):
        return 'mutation_%s'%id(self)


def dispatch(name, type_name, *args, **kwargs):
    if name not in _mutation:
        raise ValueError('%s mutation module not found'%name)

    return getattr(_mutation[name](), type_name)(*args, **kwargs)


def register_dispatch(name, type_name):
    def outwrapper(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return dispatch(name, type_name, *args, **kwargs)

        return wrapper
    return outwrapper