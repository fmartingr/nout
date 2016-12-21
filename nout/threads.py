import logging
import threading

from .singleton import Singleton


logger = logging.getLogger(__name__)


class Threads(metaclass=Singleton):
    threads = {}

    def create_thread(self, name, target, daemon=False, autostart=True):
        assert name not in self.threads, "Tried to create thread %s twice" % name
        logger.info('Creating thread %s' % name)
        self.threads[name] = threading.Thread(
            name='Thread-' + name,
            target=target,
            daemon=daemon)

        if autostart:
            self.threads[name].start()

        return self.threads[name]

    def start_thread(self, name):
        if not self.threads[name].is_alive():
            self.threads[name].start()
        else:
            logger.warning('Tried to start thread %s twice' % name)
