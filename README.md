# WFP GeoNode

This is the the WFP GeoNode customization, obtained from a GeoNode custom 
project.

## Installation

First, clone the repository:

    git clone ssh://git@codeassist.wfp.org:7999/omep/wfp-geonode.git
    
Create a virtualenv and activate it:

    virtualenv --no-site-packages env
    . env/bin/activate
    
Install WFP GeoNode with:

    cd wfp-geonode
    pip install -r requirements.txt
    pip install -e .
    





