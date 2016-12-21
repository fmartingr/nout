from datetime import datetime
import os
import os.path

from nout.conf import config


class BaseObject:
    _caches = {}

    # Cache for fields that need conversion
    def _add_attr_cache(self, key, value):
        self._caches[key] = value

    def _reset_caches(self):
        self._caches = {}


class File(BaseObject):
    def __init__(self, path):
        self.path = path
        self.relative_path = self.get_relative_path(self.path)

        # If file exists (maybe it's deleted!)
        if os.path.isfile(self.path):
            self.sync()

    def sync(self):
        self._reset_caches()
        self.filename = os.path.basename(self.path)
        self.stat = os.stat(self.path)

    @classmethod
    def get_relative_path(cls, path):
        return path.replace(config.path, '')

    @property
    def creation_time(self):
        if 'creation_time' not in self._caches:
            self._add_attr_cache('creation_time',
                                 datetime.fromtimestamp(self.stat.st_ctime))
        return self._caches['creation_time']

    @property
    def modification_time(self):
        if 'modification_time' not in self._caches:
            self._add_attr_cache('modification_time',
                                 datetime.fromtimestamp(self.stat.st_mtime))
        return self._caches['modification_time']

    @property
    def accessed_time(self):
        if 'accessed_time' not in self._caches:
            self._add_attr_cache('accessed_time',
                                 datetime.fromtimestamp(self.stat.st_atime))
        return self._caches['accessed_time']

    @property
    def __dict__(self):
        return {
            'filename': self.filename,
            'relative_path': self.relative_path,
            'creation_time': self.creation_time,
            'modification_time': self.modification_time,
            'accessed_time': self.accessed_time,
        }

    def __repr__(self):
        return str('<File %s>' % self.relative_path)
