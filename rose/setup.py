# -*- coding: utf-8 -*-
__revision__ = "$Id: $"

import sys
import os

from setuptools import setup, find_packages
from openalea.deploy.metainfo import read_metainfo

# Reads the metainfo file
metadata = read_metainfo('metainfo.ini', verbose=True)
for key,value in metadata.iteritems():
    exec("%s = '%s'" % (key, value))

#The metainfo files must contains
# version, release, project, name, namespace, pkg_name,
# description, long_description,
# authors, authors_email, url and license
# * version is 0.8.0 and release 0.8
# * project must be in [openalea, vplants, alinea]
# * name is the full name (e.g., Alinea.Rose) whereas pkg_name is only 'rose'

# Packages list, namespace and root directory of packages

pkg_name = name.lower()
src_rep = 'rose'
packages =[ namespace+'.rose']+ [namespace+'.rose.'+m for m in find_packages(src_rep)]
package_dir = {pkg_name : src_rep}
# List of top level wralea packages (directories with __wralea__.py)
#wralea_entry_points = ['%s = %s'%(pkg,namespace + '.' + pkg) for pkg in top_pkgs]

# dependencies to other eggs
setup_requires = ['openalea.deploy']
if("win32" in sys.platform):
    install_requires = []
else:
    install_requires = []

# web sites where to find eggs
dependency_links = ['http://openalea.gforge.inria.fr/pi']

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
    package_dir= package_dir,

    # Namespace packages creation by deploy
    namespace_packages = [namespace],
    create_namespaces = True,
    zip_safe= False,

    # Dependencies
    setup_requires = setup_requires,
    install_requires = install_requires,
    dependency_links = dependency_links,


    include_package_data = True,
    package_data = {'' : ['*.mtg', '*.drf', '*.txt', '*.csv'],},

    # Declare scripts and wralea as entry_points (extensions) of your package
    entry_points = {'wralea' : ['rose = alinea.rose','rose.mockup = alinea.rose.mockup','rose.growth = alinea.rose.growth'],},
    )


