import logging
import fnmatch
import os
import os.path

from watchdog import events as watchdog_events

from .conf import config
from .objects import File
from .singleton import Singleton
from .storage import DatabaseStorage


logger = logging.getLogger(__name__)


class Tree(metaclass=Singleton):
    def __init__(self, enable_database=True):
        self.files = {}
        self.ignore_patterns = config.ignore_patterns

        if enable_database:
            self.database = DatabaseStorage()

    @property
    def database_enabled(self):
        return getattr(self, 'database', False)

    def matches_ignore_patterns(self, filename):
        return any([fnmatch.fnmatchcase(filename, pattern)
                    for pattern in self.ignore_patterns])

    def read(self):
        for root, subdirs, files in os.walk(config.path):
            for f in files:
                if not self.matches_ignore_patterns(f):
                    file_path = os.path.join(root, f)
                    self.add_file(file_path)

    def add_file(self, path):
        file_object = File(path, stat=True)
        self.files[file_object.relative_path] = file_object
        if self.database_enabled:
            self.database.add_to_queue('create', file_object)

    def delete_file(self, path):
        file_object = File(path, stat=False)
        if file_object.relative_path in self.files:
            del self.files[file_object.relative_path]
            if self.database_enabled:
                self.database.add_to_queue(
                    'remove', self.files[file_object.relative_path])

    def update_file(self, path):
        pass


class EventHandler(watchdog_events.FileSystemEventHandler):
    def on_created(self, event):
        path = event.src_path
        if isinstance(event, watchdog_events.FileCreatedEvent):
            if not Tree().matches_ignore_patterns(os.path.basename(path)):
                logger.info('File created: %s' % path)
                Tree().add_file(path)

    def on_deleted(self, event):
        path = event.src_path
        if isinstance(event, watchdog_events.FileDeletedEvent):
            if not Tree().matches_ignore_patterns(os.path.basename(path)):
                logger.info('File deleted: %s' % path)
                Tree().delete_file(path)
