import dataset
import logging
import queue

from .conf import config
from .threads import Threads
from .singleton import Singleton

threads = Threads()
logger = logging.getLogger(__name__)


class DatabaseStorage(metaclass=Singleton):
    def __init__(self):
        self._queue = queue.Queue()
        self._thread = threads.create_thread(
            name='Database',
            target=self.thread_worker,
            daemon=True)

    def connect(self):
        self.db = dataset.connect(
            'sqlite:///' + config.path + '/.nout.sqlite')
        self.table = self.db['notes']
        self.setup_database()

    def add_to_queue(self, action, file_object):
        self._queue.put({
            'action': action,
            'file_object': file_object})

    def thread_worker(self):
        self.connect()
        while True:
            item = self._queue.get()
            logger.info('Queue received: %s' % item['file_object'].relative_path)
            if item['action'] == 'create':
                self.upsert(item['file_object'])
            if item['action'] == 'remove':
                self.remove(item['file_object'])
            self._queue.task_done()

    def setup_database(self):
        self.table.create_index(['relative_path', 'filename'])

    def upsert(self, file_object):
        self.table.upsert(file_object.__dict__, ['relative_path'])

    def remove(self, file_object):
        self.table.delete(relative_path=file_object.relative_path)
