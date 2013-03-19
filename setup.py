import os
from setuptools import setup

def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)
  
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir != '':
    os.chdir(root_dir)
django_dir = 'django'

for dirpath, dirnames, filenames in os.walk(django_dir):
# Ignore PEP 3147 cache dirs and those whose names start with '.'
    dirnames[:] = [d for d in dirnames if not d.startswith('.') and d != '__pycache__']
    if '__init__.py' in filenames:
        packages.append('.'.join(fullsplit(dirpath)))
    elif filenames:
        data_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames]])

setup(
    name="pybab",
    version=open("VERSION").read().strip('\n'),
    description=open("README.md", 'r').read(),
    url="https://github.com/MPBAUnofficial/pybab",
    author="Roberto Bampi",
    author_email="robampi@fbk.eu",
    packages=packages,
    data_files=data_files,
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: GPL License',
        'Operating System :: OS Indipendent',
        'Framework :: Django',
    ],
    install_requires=["django", "hive", "django-tojson"],
    dependency_links=["https://github.com/MPBAUnofficial/hive/tarball/develop#egg=hive",
                      "https://github.com/davidek/django-tojson/tarball/master#egg=django-tojson"]
)

