from __future__ import absolute_import, division, print_function, with_statement

import os, time, base64
from copy import deepcopy
try:
    import cPickle as pickle
except ImportError:
    import pickle
try:
    import hashlib
    sha1 = hashlib.sha1
except ImportError:
    import sha
    sha1 = sha.new

from tornado.util import ObjectDict

from turbo.conf import app_config
from turbo.log import session_log


class Session(object):

    __slots__ = ['store', 'handler', 'app', '_data', '_dirty', '_config',
        '_initializer', 'session_id', '_session_object', '_session_name']

    def __init__(self, app, handler, store, initializer, session_config=None, session_object=None):
        self.handler = handler
        self.app = app
        self.store = store or DiskStore(app_config.store_config.diskpath)

        self._config = deepcopy(app_config.session_config)
        if session_config:
            self._config.update(session_config)

        self._session_name = self._config.name

        self._session_object = (session_object or CookieObject)(app, handler, self.store, self._config)
        
        self._data = ObjectDict()
        self._initializer = initializer

        self.session_id = None

        self._dirty = False
        self._processor()

    def __getitem__(self, name):
        if name not in self._data:
            session_log.error('%s key not exist in %s session' % (name, self.session_id))

        return self._data.get(name, None)

    def __setitem__(self, name, value):
        self._data[name] = value
        self._dirty = True

    def __delitem__(self, name):
        del self._data[name]
        self._dirty = True

    def __contains__(self, name):
        return name in self._data

    def __len__(self):
        return len(self._data)

    def __getattr__(self, name):
        return getattr(self._data, name)
    
    def __setattr__(self, name, value):
        if name in self.__slots__:
            super(Session, self).__setattr__(name, value)
        else:
            self._dirty = True
            setattr(self._data, name, value)
        
    def __delattr__(self, name):
        delattr(self._data, name)
        self._dirty = True

    def __iter__(self):
        for key in self._data:
            yield key

    def __repr__(self):
        return str(self._data)

    def _processor(self):
        """Application processor to setup session for every request"""
        self.store.cleanup(self._config.timeout)
        self._load()

    def _load(self):
        """Load the session from the store, by the id from cookie"""

        self.session_id = self._session_object.get_session_id()

        # protection against session_id tampering
        if self.session_id and not self._valid_session_id(self.session_id):
            self.session_id = None

        if self.session_id:
            d = self.store[self.session_id]
            if isinstance(d, dict) and d:
                self.update(d)

        if not self.session_id:
            self.session_id = self._session_object.generate_session_id()

        if not self._data:
            if self._initializer and isinstance(self._initializer, dict):
                self.update(deepcopy(self._initializer))

        self._session_object.set_session_id(self.session_id)

    def save(self):
        if self._dirty:
            self.store[self.session_id] = self._data

    def _valid_session_id(self, session_id):
        return True

    def kill(self):
        """Kill the session, make it no longer available"""
        del self.store[self.session_id]

    def clear(self):
        del self.store[self.session_id]


class SessionObject(object):


    def __init__(self, app, handler, store, session_config):
        self.app = app
        self.handler = handler
        self.store = store

        self._config = deepcopy(app_config.session_config)
        if session_config:
            self._config.update(session_config)

        self._session_name = self._config.name

    def get_session_id(self):
        raise NotImplementedError

    def set_session_id(self, session_id):
        raise NotImplementedError

    def clear_session_id(self):
        raise NotImplementedError

    def generate_session_id(self):
        """Generate a random id for session"""
        secret_key = self._config.secret_key
        while True:
            rand = os.urandom(16)
            now = time.time()
            session_id = sha1("%s%s%s%s" %(rand, now, self.handler.request.remote_ip, secret_key))
            session_id = session_id.hexdigest()
            if session_id not in self.store:
                break

        return session_id


class CookieObject(SessionObject):

    def set_session_id(self, session_id):
        self._set_cookie(self._session_name, session_id)

    def get_session_id(self):
        return self._get_cookie(self._session_name)

    def clear_session_id(self):
        self.handler.clear_cookie(self._session_name)

    def _set_cookie(self, name, value):
        cookie_domain = self._config.cookie_domain
        cookie_path = self._config.cookie_path
        cookie_expires = self._config.cookie_expires
        if self._config.secure:
            return self.handler.set_secure_cookie(name, value,
                expires_days=cookie_expires/(3600*24), domain=cookie_domain, path=cookie_path)
        else:
            return self.handler.set_cookie(name, value, expires=cookie_expires, domain=cookie_domain, path=cookie_path)
    
    def _get_cookie(self, name):
        if self._config.secure:
            return self.handler.get_secure_cookie(name)
        else:
            return self.handler.get_cookie(name)


class HeaderObject(SessionObject):

    def get_session_id(self):
        return self.handler.request.headers.get(self._session_name)

    def set_session_id(self, sid):
        self.handler.set_header(self._session_name, sid)

    def clear_session_id(self):
        self.handler.clear_header(self._session_name)


class Store(object):

    """Base class for session stores"""

    def __contains__(self, key):
        raise NotImplementedError

    def __getitem__(self, key):
        raise NotImplementedError

    def __setitem__(self, key, value):
        raise NotImplementedError

    def cleanup(self, timeout):
        """removes all the expired sessions"""
        raise NotImplementedError

    def encode(self, session_data):
        """encodes session dict as a string"""
        pickled = pickle.dumps(session_data)
        return base64.encodestring(pickled)

    def decode(self, session_data):
        """decodes the data to get back the session dict """
        pickled = base64.decodestring(session_data)
        return pickle.loads(pickled)


class DiskStore(Store):
    """
    Store for saving a session on disk.

        >>> import tempfile
        >>> root = tempfile.mkdtemp()
        >>> s = DiskStore(root)
        >>> s['a'] = 'foo'
        >>> s['a']
        'foo'
        >>> time.sleep(0.01)
        >>> s.cleanup(0.01)
        >>> s['a']
        Traceback (most recent call last):
            ...
        KeyError: 'a'
    """
    def __init__(self, root):
        # if the storage root doesn't exists, create it.
        if not os.path.exists(root):
            os.makedirs(
                    os.path.abspath(root)
                    )
        self.root = root

    def _get_path(self, key):
        if os.path.sep in key: 
            raise ValueError, "Bad key: %s" % repr(key)
        return os.path.join(self.root, key)
    
    def __contains__(self, key):
        path = self._get_path(key)
        return os.path.exists(path)

    def __getitem__(self, key):
        path = self._get_path(key)
        if os.path.exists(path): 
            pickled = open(path).read()
            return self.decode(pickled)
        else:
            return ObjectDict()

    def __setitem__(self, key, value):
        path = self._get_path(key)
        pickled = self.encode(value)    
        try:
            f = open(path, 'w')
            try:
                f.write(pickled)
            finally: 
                f.close()
        except IOError:
            pass

    def __delitem__(self, key):
        path = self._get_path(key)
        if os.path.exists(path):
            os.remove(path)
    
    def cleanup(self, timeout):
        now = time.time()
        for f in os.listdir(self.root):
            path = self._get_path(f)
            atime = os.stat(path).st_atime
            if now - atime > timeout :
                os.remove(path)


class RedisStore(Store):

    def __init__(self, **kwargs):
        self.timeout = kwargs.get('timeout') or app_config.session_config.timeout

    def __contains__(self, key):
        return self.get_connection(key).exists(key)

    def __setitem__(self, key, value):
        conn = self.get_connection(key)
        conn.hset(key, 'data', self.encode(value))
        conn.expire(key, self.timeout)

    def __getitem__(self, key):
        data = self.get_connection(key).hget(key, 'data')
        if data:
            return self.decode(data)
        else:
            return ObjectDict()

    def __delitem__(self, key):
        self.get_connection(key).delete(key)

    def cleanup(self, timeout):
        pass

    def get_connection(self, key):
        import redis
        return redis.Redis()