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
    long_description=(read('README.rst')),
    # Full list of classifiers can be found at:
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 1 - Planning',
    ],
    license="BSD",
    keywords="wfp geonode django",
    url='https://github.com/wfp/wfp',
    packages=['wfp',],
    include_package_data=True,
    install_requires=[
        'django-tastypie==0.11.0',
        'psycopg2==2.5.3',
        'python-memcached==1.53',
        'raven',
        'django-celery==3.1.10',
    ],
    zip_safe=False,
)
