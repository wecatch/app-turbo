from __future__ import absolute_import, division, print_function, with_statement

import os
import time
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

    def __init__(self, app, handler, store):
        self.store = store
        self.handler = handler
        self.app = app

        self._data = ObjectDict()
        self._last_cleanup_time = 0
        self._config = app_config.session_config['cookie']
        self.__getitem__ = self._data.__getitem__
        self.__setitem__ = self._data.__setitem__
        self.__delitem__ = self._data.__delitem__

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

    def _load(self):
        """Load the session from the store, by the id from cookie"""

        # protection against session_id tampering
        if self.session_id and not self._valid_session_id(self.session_id):
            self.session_id = None

        self._check_expiry()

    def _check_expiry(self):
        # check for expiry
        if self.session_id and self.session_id not in self.store:
            if self._config.ignore_expiry:
                self.session_id = None
            else:
                return self.expired()

    def expired(self):
        """Called when an expired session is atime"""
        self._killed = True
        self._save()
        raise SessionExpired(self._config.expired_message)

    def _save(self):
        if not self.get('_killed'):
            self._setcookie(self.session_id)
            self.store[self.session_id] = dict(self._data)
        else:
            self._setcookie(self.session_id, expires=-1)

    def _valid_session_id(self):
        return True

    def _setcookie(self, session_id, expires='', **kw):
        cookie_name = self._config.cookie_name
        cookie_domain = self._config.cookie_domain
        cookie_path = self._config.cookie_path
        secure = self._config.secure
        if secure:
            self.handler.set_secure_cookie(cookie_name, session_id, expires=expires, domain=cookie_domain, path=cookie_path, **kwargs)
        else:
            self.handler.set_cookie()

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
            raise KeyError, key

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


