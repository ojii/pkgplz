import ast
import json
import os
import setuptools


def detect_name(root):
    src = os.path.join(root, 'src')
    for name in os.listdir(src):
        if '.' in name:
            continue
        path = os.path.join(src, name)
        if not os.path.isdir(path):
            continue
        init = os.path.join(path, '__init__.py')
        if not os.path.exists(init):
            continue
        return name


def _dunders(module):
    for node in module.body:
        if not isinstance(node, ast.Assign):
            continue
        if len(node.targets) != 1:
            continue
        if not isinstance(node.targets[0], ast.Name):
            continue
        name = node.targets[0].id
        if not name.startswith('__'):
            continue
        if not name.endswith('__'):
            continue
        if not isinstance(node.value, ast.Str):
            continue
        yield name.strip('_'), node.value.s


def get_dunders(root, name):
    with open(os.path.join(root, 'src', name, '__init__.py')) as fobj:
        module = ast.parse(fobj.read())
    return dict(_dunders(module))


def get(key, *dicts):
    for d in dicts:
        if key in d:
            return d[key]
    return None


def read_requirements(root, name):
    path = os.path.join(root, name)
    if not os.path.exists(path):
        return []
    with open(path) as fobj:
        for line in filter(bool, map(str.strip, fobj.readlines())):
            if line.startswith(('#', '-')):
                continue
            if '#' in line:
                line = line.split('#', 1)[0].strip()
            yield line


def package_please(filename):
    root = os.path.abspath(os.path.dirname(filename))
    config = os.path.join(root, 'setup.json')
    if os.path.exists(config):
        with open(config) as fobj:
            extra = json.load(fobj)
    else:
        extra = {}

    name = extra.get('name', detect_name(root))

    dunders = get_dunders(root, name)

    setuptools.setup(
        name=name,
        version=dunders['version'],
        license=dunders.get('license', None),
        url=dunders.get('uri', None),
        author=dunders.get('author', None),
        author_email=dunders.get('author_email', None),
        packages=setuptools.find_packages(where=os.path.join(root, 'src')),
        package_dir={'': 'src'},
        zip_safe=False,
        install_requires=read_requirements(root, 'requirements.txt'),
        test_requires=read_requirements(root, 'test_requirements.txt'),
        entry_points={
            'console_scripts': [
                list(
                    map(
                        '%s = %s'.__mod__,
                         extra.get('console_scripts', {}).items()
                    )
                )
            ]
        },
    )


package_please(__file__)
