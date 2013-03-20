import os
from setuptools import setup, find_packages

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="pybab",
    version=open("VERSION").read().strip('\n'),
    description=open("README.md", 'r').read(),
    url="https://github.com/MPBAUnofficial/pybab",
    author="Roberto Bampi",
    author_email="robampi@fbk.eu",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: GPL License',
        'Operating System :: OS Indipendent',
        'Framework :: Django',
    ],
    install_requires=["django", "pyhive==0.2.0", "django-tojson==0.3.0"],
    dependency_links=["http://github.com/MPBAUnofficial/pyhive/tarball/develop#egg=pyhive-0.2.0",
                      "http://github.com/davidek/django-tojson/tarball/master#egg=django-tojson-0.3.0"]
)

