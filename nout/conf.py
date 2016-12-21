import os.path


class Config:
    path = os.path.expanduser('~/Notes')
    ignore_patterns = (
        '*~',
        '.*',
    )


config = Config()
