from __future__ import absolute_import

import json
import os

import click

from . import runtime


@click.group()
def main():
    pass


@main.command()
def init():
    with open(runtime.__file__) as fobj:
        runtime_code = fobj.read()
    with open('setup.py', 'w') as fobj:
        fobj.write(runtime_code)
        fobj.write('\n\npackage_please(__file__)\n')
    with open('setup.json', 'w') as fobj:
        json.dump({}, fobj)


@main.command(name='add-script')
@click.argument('name')
@click.argument('location')
def add_script(name, location):
    if os.path.exists('setup.json'):
        with open('setup.json') as fobj:
            extra = json.load(fobj)
    else:
        extra = {}
    if 'console_scripts' not in extra:
        extra['console_scripts'] = {}
    extra['console_scripts'][name] = location
    with open('setup.json', 'w') as fobj:
        json.dump(extra, fobj)
