from distutils.core import setup

setup(
    name="pybab",
    version=open("VERSION").read().strip('\n'),
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
    requires=["django"],
    # Install hive and tojson by hand
    #dependency_links=["https://github.com/MPBAUnofficial/hive/tarball/develop#egg=hive"]
)

