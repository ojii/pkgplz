# Package Please

The tool for when you finally give up on writing setup.py files and just want
a package, please.

# Usage

## Prerequisites

`pip install pkgplz`. Your code must be in `src/<pkgname>/...`. In your `__init__.py`
(`src/<pkgname>/__init__.py`) you must specify your version using `__version__ = '...'`.
You can also specify `__author__`, `__author_email__`, `__uri__` and `__license__`.
All values must be static strings.

## Getting started

Run `pkgplz init` in your project root. You now have a `setup.py` that should work.

## Console scripts

Run `pkgplz add-script <name> <import-path>`.

## Requirements

Dump requirements into a `requirements.txt`, if you want extra test requirements,
add them to `test_requirments.txt`.
