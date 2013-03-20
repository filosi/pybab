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
    install_requires=["django", "pyhive", "django-tojson"],
    dependency_links=["git+http://github.com/MPBAUnofficial/pyhive.git@develop#egg=pyhive",
                      "git+http://github.com/davidek/django-tojson@master#egg=django-tojson"]
)

