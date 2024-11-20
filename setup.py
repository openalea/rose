# -*- coding: utf-8 -*-

import sys

from setuptools import setup, find_namespace_packages

# Define the metainfo file

name = "OpenAlea.RoseMockup"
authors='Hervé Autret, Jessica Bertheloot, Christophe Pradal'
authors_email='christophe.pradal at cirad dot fr'
description='3D reconstruction of roses'
long_description=description
url = 'https://github.com/openalea/rosemockup'
license= 'CeCILL-C'

# find version number in src/openalea/mtg/version.py
_version = {}
with open("src/openalea/rose/version.py") as fp:
    exec(fp.read(), _version)

version = _version["__version__"]
# Packages list, namespace and root directory of packages

pkg_name = name.lower()
packages =find_namespace_packages(where='src', include=['openalea.*'])

# dependencies to other eggs
setup_requires = ['openalea.deploy']
if("win32" in sys.platform):
    install_requires = []
else:
    install_requires = []

# web sites where to find eggs
#dependency_links = ['http://openalea.gforge.inria.fr/pi']

setup(
    name=name,
    version=version,
    description=description,
    long_description=long_description,
    author=authors,
    author_email=authors_email,
    url=url,
    license=license,
    keywords = '',

    # package installation
    packages= packages,
    package_dir={'': 'src'},

    # Namespace packages creation by deploy
    zip_safe= False,


    include_package_data = True,
    package_data = {'' : ['*.mtg', '*.drf', '*.txt', '*.csv'],},

    # Declare scripts and wralea as entry_points (extensions) of your package
    entry_points = {'wralea' : ['rose = openalea.rose','rose.mockup = openalea.rose.mockup'],},
    )


