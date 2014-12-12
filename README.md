# WFP GeoNode

This is the the WFP GeoNode customization, obtained from a GeoNode custom 
project.

## Installation

First, clone the repository:

    git clone ssh://git@codeassist.wfp.org:7999/omep/wfp-geonode.git
    
Create a virtualenv:

    virtualenv --no-site-packages env

Create the geonode django and uploads databases using postgres and postgis 
(you can restore them from dumps or populate them with syncdb).

Setup the needed environment variables, for example add an envars file with the
following content, changing it accordingly to your environemnt:

    export secret_key='***'
    export site_url=http://localhost:8000/
    export geonode_user=gnadmin
    export geonode_pwd=***
    export geonode_django_db=sdi_django
    export geonode_postgis_db=sdi_uploads
    export geoserver_user=admin
    export geoserver_pwd=geoserver
    export geoserver_url=http://localhost:8080/geoserver/
    export email_host='smtp.gmail.com'
    export email_host_user='wfp.geonode@gmail.com'
    export email_host_password='***'

Now source the file in the env/bin/activate script and activate the 
virtualenv:

    . env/bin/activate
    
Install WFP GeoNode with:

    cd wfp-geonode
    $ pip install -e .
    
In case you want to test WFP GeoNode with the Django development server, edit 
the local_settings.py file, and set DEBUG_STATIC = True.

Now run the Django development server and enjoy GeoNode!






