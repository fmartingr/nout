import time
import logging

from watchdog.observers import Observer

from .conf import config
from .tree import EventHandler
from .threads import Threads


logger = logging.getLogger(__name__)
threads = Threads()


class FileWatcher:
    def __init__(self):
        self.observer = Observer()
        self._thread = threads.create_thread(
            name='Watcher',
            target=self.run,
            daemon=True)

    def run(self):
        event_handler = EventHandler()
        self.observer.schedule(event_handler, config.path, recursive=True)
        self.observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()
