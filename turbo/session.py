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


class Session(object):

    __slots__ = ['store', 'handler', 'app', '_data', '_initializer', '_session_object'
        '__getitem__', '__setitem__', '__delitem__']

    def __init__(self, app, handler, store, initializer, session_config=None, session_object=None):
        self.store = store
        self.handler = handler
        self.app = app

        self._data = ObjectDict()
        self._initializer = initializer

        self._config = app_config.session_config if session_config is None else session_config 
        self._session_name = self._config.name
        self._session_object = session_object if isinstance(session_object, SessionObject) else CookieObject(app, handler, self._config)

        self.__getitem__ = self._data.__getitem__
        self.__setitem__ = self._data.__setitem__
        self.__delitem__ = self._data.__delitem__
        self._processor()

    def __contains__(self, name):
        return name in self._data

    def __getattr__(self, name):
        return getattr(self._data, name)
    
    def __setattr__(self, name, value):
        if name in self.__slots__:
            super(Session, self).__setattr__(self, name, value)
        else:
            setattr(self._data, name, value)
        
    def __delattr__(self, name):
        delattr(self._data, name)

    def _processor(self):
        """Application processor to setup session for every request"""
        #self._cleanup() TODO clean timeout session from store
        self._load()

    def _load(self):
        """Load the session from the store, by the id from cookie"""

        self.session_id = self._session_object.get_session_id()

        # protection against session_id tampering
        if self.session_id and not self._valid_session_id(self.session_id):
            self.session_id = None

        if self.session_id:
            d = self.store[self.session_id]
            self.update(d)

        if not self.session_id:
            self.session_id = self._generate_session_id()

            if self._initializer and isinstance(self._initializer, dict):
                self.update(deepcopy(self._initializer))

    def _save(self):
        if not self.get('_killed'):
            self._session_object.set_session_id(self.session_id)
            self.store[self.session_id] = dict(self._data)
        else:
            self._session_object.set_session_id(self.session_id)

    def _valid_session_id(self, session_id):
        return True

    # def _cleanup(self):
    #     """Cleanup the stored sessions"""
    #     current_time = time.time()
    #     timeout = self._config.timeout
    #     if current_time - self._last_cleanup_time > timeout:
    #         self.store.cleanup(timeout)
    #         self._last_cleanup_time = current_time

    def _generate_session_id(self):
        """Generate a random id for session"""

        while True:
            rand = os.urandom(16)
            now = time.time()
            secret_key = self._config.secret_key
            session_id = sha1("%s%s%s%s" %(rand, now, self.handler.request.remote_ip, secret_key))
            session_id = session_id.hexdigest()
            if session_id not in self.store:
                break
        return session_id

    def kill(self):
        """Kill the session, make it no longer available"""
        del self.store[self.session_id]


class SessionObject(object):


    def __init__(self, app, handler, session_config):
        self.app = app
        self.handler = handler
        self._config = session_config
        self._session_name = self._config.name

    def get_session_id(self):
        raise NotImplementedError

    def set_session_id(self, session_id, **kwargs):
        raise NotImplementedError

    def clear_session_id(self):
        raise NotImplementedError


class CookieObject(SessionObject):

    def set_session_id(self, session_id, **kwargs):
        cookie_domain = self._config.cookie_domain
        cookie_path = self._config.cookie_path
        expires = self._config.expires 
        self._set_cookie(self._session_name, session_id, expires=expires, domain=cookie_domain, path=cookie_path, **kwargs)

    def get_session_id(self):
        return self._get_cookie(self._session_name)

    def clear_session_id(self):
        self.handler.clear_cookie(self._session_name)

    @property
    def _set_cookie(self):
        if self._config.secure:
            return self.handler.set_secure_cookie
        else:
            return self.handler.set_cookie

    @property
    def _get_cookie(self):
        if self._config.secure:
            return self.handler.get_secure_cookie
        else:
            return self.handler.get_cookie



class HeaderSessionIdTransmission(object):

    def get_session_id(self):
        return self.handler.request.headers.get(self._session_name)

    def set_session_id(self, sid):
        self.handler.set_header(self._session_name, sid)

    def clear_session_id(self):
        pass



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

    def encode(self, session_dict):
        """encodes session dict as a string"""
        pickled = pickle.dumps(session_dict)
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


