from django.conf.urls import patterns, url, include
import views

from geonode.urls import urlpatterns
#from djgeojson.views import GeoJSONLayerView

from gis.models import Employee
#from gis.views import employees_geojson
from gis.views import EmployeeLayer

urlpatterns = patterns('',

    # Static pages
    url(r'^$', views.index, name='home'),
    url(r'^contacts/$', views.contacts, name='contacts'),
    # OWS proxy
    url(r'^owslogin/$', views.owslogin, name='owslogin'),
    # WFP documents views
    (r'^wfpdocs/', include('wfp.wfpdocs.urls')),
    # WFP people views
    url(r'^gis/employees.geojson$', 
        EmployeeLayer.as_view(model=Employee,
            properties=(
                ['gis_level', 'place', 'country', 'wfpregion', 'facility',
                 'name', 'position']
            )),
            name='employees-geojson'),
    #url(r'^gis/employees_old.geojson$', employees_geojson, name='employees-geojson-old')
 ) + \
urlpatterns
