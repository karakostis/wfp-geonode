#!/usr/bin/env python
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
