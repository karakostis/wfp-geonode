import os
from distutils.core import setup

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
    name="wfp",
    version="0.2",
    author="",
    author_email="",
    description="wfp, based on GeoNode",
    long_description=(read('README.md')),
    # Full list of classifiers can be found at:
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 1 - Planning',
    ],
    license="BSD",
    keywords="wfp geonode django",
    url='http://geonode.wfp.org',
    packages=['wfp',],
    include_package_data=True,
    install_requires=[
        'django-tastypie==0.11.0',
        'psycopg2==2.5.3',
        'python-memcached==1.53',
        'raven==5.0.0',
        'django-celery==3.1.10',
        'django-supervisor==0.3.2',
        'Pillow==2.3.0',
        'supervisor==3.1.0',
        'Wand==0.3.8',
    ],
    zip_safe=False,
)
