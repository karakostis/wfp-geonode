# WFP GeoNode

This is a WFP customization GeoNode, obtained from a GeoNode custom 
project. It is currently in production at http://geonode.wfp.org

# Links

   * Project home page: http://codeassist.wfp.org/stash/projects/GEONODE/repos/wfp-geonode/browse
   * Issue tracker: http://codeassist.wfp.org/jira/browse/GEONODE
   * Download: http://pypi.wfp.org/packages/wfp-geonode/
   * Docs: http://readthedocs.wfp.org/docs/wfp-geonode/en/latest/
   * CI: http://ci.wfp.org/job/wfp-geonode/
   * Confluence: http://codeassist.wfp.org/confluence/display/OMEP/GeoNode

## Installation

First, clone the repository:

    git clone ssh://git@codeassist.wfp.org:7999/geonode/wfp-geonode.git
    
Create a virtualenv:

    virtualenv --no-site-packages env

Create the geonode django and uploads databases using postgres and postgis 
(you can restore them from dumps or populate them with syncdb).

Copy the wfp/settings/_capooti.py file to wfp/settings/_yourusername.py

Add in _yourusername anything more you want to install, for example the Django toolbar.

Activate the virtualenv:

    . env/bin/activate
    
Install WFP GeoNode with:

    cd wfp-geonode
    pip install -e .

Setup the needed configuration file, tipically in ~/.wfp-geonode_credentials.json (this should be created automatically at application startup, but you still need to set correct credentials)

In case you want to test WFP GeoNode with the Django development server, edit 
the local_settings.py file, and set DEBUG_STATIC = True.

Now run the Django development server and enjoy GeoNode!

To run tests:

    paver run_tests







