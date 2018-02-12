import os.path

from .singleton import Singleton


class Config(metaclass=Singleton):
    path = os.path.expanduser('~/Notes')
    ignore_patterns = (
        '*~',
        '.*',
    )


config = Config()
