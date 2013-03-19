from setuptools import setup

setup(
    name="hive",
    version=open("VERSION").read(),
    description=open("README.md", 'r').read(),
    url="https://github.com/MPBAUnofficial/pybab",
    author="Roberto Bampi",
    author_email="robampi@fbk.eu",
    packages=["pybab"],
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: GPL License',
        'Operating System :: OS Indipendent',
        'Framework :: Django',
    ],
    requires=["django", "hive"],
    dependency_links=["https://github.com/MPBAUnofficial/hive/tarball/develop#egg=hive"]
)

