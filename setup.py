#!/usr/bin/env python
#########################################################################
#
# Copyright (C) 2012-2015 Paolo Corti, pcorti@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################

import os
import codecs
from distutils.config import PyPIRCCommand
from setuptools import setup, find_packages

dirname = 'wfp'
app = __import__(dirname)

def read(*parts):
    here = os.path.abspath(os.path.dirname(__file__))
    return codecs.open(os.path.join(here, *parts), 'r').read()

PyPIRCCommand.DEFAULT_REPOSITORY = 'http://pypi.wfp.org/pypi/'

setup(
    name=app.NAME,
    version=app.get_version(),
    url='http://codeassist.wfp.org/stash/projects/GEONODE/repos/wfp-geonode/browse',
    
    author='UN World Food Programme',
    author_email='hq.gis@wfp.org',
    license="WFP Property",
    description='WFP GeoNode',

    packages=find_packages('.'),
    include_package_data=True,
    dependency_links=['http://pypi.wfp.org/simple/'],
    install_requires=read('wfp/requirements/install.pip'),
    platforms=['linux'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Developers'
    ],
    long_description=open('README.md').read()
)
