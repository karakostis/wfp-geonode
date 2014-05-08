How to use the API
==================

Request the full list of API for the gis application::

    http://localhost:8000/gis/api/v1/?format=json
    
WFP Offices
-----------

Request office schema::

    http://localhost:8000/gis/api/v1/office/schema/?format=json
    
Request the full offices list::

    http://localhost:8000/gis/api/v1/office/?format=json
    
Include geojson parameter if you want properly geojson output!::

    http://localhost:8000/gis/api/v1/office/?format=json&geojson

Request just one office (id=1)::

    http://localhost:8000/gis/api/v1/office/1/?format=json

Request the a set of offices (id=1 and id=3)::

    http://localhost:8000/gis/api/v1/office/set/1;3/?format=json
    
Request offices for a given place::

    http://localhost:8000/gis/api/v1/office/?format=json&place=Rome
    
Request offices for a certain status::

    http://localhost:8000/gis/api/v1/office/?format=json&status=Closed
    
Request offices for certain WFP region::

    http://localhost:8000/gis/api/v1/office/?format=json&wfpregion=OMC
    
Full reference for query syntax::

    https://docs.djangoproject.com/en/dev/topics/db/queries/
    
WFP Employees
-------------

Request employee schema::

    http://localhost:8000/gis/api/v1/employee/schema/?format=json
    
Include geojson parameter if you want properly geojson output!::

    http://localhost:8000/gis/api/v1/employee/?format=json&geojson

Request the full employees list::

    http://localhost:8000/gis/api/v1/employee/?format=json

Request just one employee (id=1)::

    http://localhost:8000/gis/api/v1/employee/1/?format=json

Request the a set of employees (id=1 and id=3)::

    http://localhost:8000/gis/api/v1/employee/set/1;3/?format=json
    
Request offices for a given place::

    http://localhost:8000/gis/api/v1/office/?format=json&place=Rome
    
Request offices for a certain status::

    http://localhost:8000/gis/api/v1/office/?format=json&status=Closed
    
Request offices for certain WFP region::

    http://localhost:8000/gis/api/v1/office/?format=json&wfpregion=OMC
    
Full reference for query syntax::

    https://docs.djangoproject.com/en/dev/topics/db/queries/
    
