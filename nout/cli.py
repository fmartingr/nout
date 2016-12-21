import logging
import sys

import click

from nout.tree import Tree
from nout.watcher import FileWatcher


logger = logging.getLogger(__file__)


@click.group()
@click.option('--info', is_flag=True)
def cli(info):
    if info:
        logging.basicConfig(level=logging.INFO)


@cli.command()
def daemon():
    click.echo('Starting Nout daemon')
    FileWatcher()  # Start watching for changes
    tree = Tree()
    tree.read()  # Read initial status

    # Start main event loop
    while True:
        try:
            pass
        except KeyboardInterrupt:
            click.echo('Exiting...')
            sys.exit(0)
