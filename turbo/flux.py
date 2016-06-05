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


class ObjectDict(dict):
    """Makes a dictionary behave like an object, with attribute-style access.
    """
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value


state = ObjectDict()


class State(object):

    __slots__ = ['_state']
    
    def __init__(self, file_attr):
        name = file_attr
        filepath = os.path.abspath(file_attr)
        if os.path.isfile(filepath):
            name, ext = os.path.splitext(os.path.basename(filepath))

        if name in state:
            raise KeyError('state %s has already existed'%name)

        self._state = ObjectDict()
        state[name] = self._state

    def __setattr__(self, name, value):
        if name in self.__slots__:
            return super(State, self).__setattr__(name, value)
            
        self._state[name] = value

    def __getattr__(self, name):
        if name not in self._state:
            raise AttributeError("%s object has no attribute '%s'"%(self.__class__.__name__, name))

        return self._state[name]


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