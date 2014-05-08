#from tastypie.resources import ModelResource
from tastypie.contrib.gis.resources import ModelResource
from tastypie import fields
from tastypie.authentication import BasicAuthentication
from tastypie.cache import SimpleCache
from tastypie.constants import ALL, ALL_WITH_RELATIONS

from geonode.people.models import Profile

from models import Office, Employee
from geojson import GeoJSONSerializer

class GisModelResource(ModelResource):
    include_resource_uri = False
    allowed_methods = ['get']
    authentication = BasicAuthentication()
    
    def serialize(self, request, data, format, options=None):
        """
        Override to parse the parameter and look for the geojson option.
        """
        options = options or {}
        options['geojson'] = request.GET and (request.GET.get('geojson','0').lower() in ['','true','1'])
        return super(ModelResource, self).serialize(request, data, format, options)
    
class OfficeResource(GisModelResource):
    
    class Meta:
        queryset = Office.objects.all()
        resource_name = 'office'
        fields = ['id', 'country', 'facility', 'place', 'source', 'status', 
            'wfpregion', 'geometry', ]
        filtering = {
            'place': ALL,
            'status': ALL,
            'wfpregion': ALL,
        }
        serializer = GeoJSONSerializer()
                 
class ProfileResource(GisModelResource):
    
    class Meta:
        queryset = Profile.objects.all()
        resource_name = 'profile'
        fields = ['name', 'position',]
        
class EmployeeResource(GisModelResource):
    
    profile = fields.ToOneField(ProfileResource, 'profile', full=True)
    office = fields.ToOneField(OfficeResource, 'office', full=True)
    
    class Meta:
        queryset = Employee.objects.all()
        resource_name = 'employee'
        include_resource_uri = False
        allowed_methods = ['get']
        authentication = BasicAuthentication()
        filtering = {
            'profile': ALL_WITH_RELATIONS,
        }
        serializer = GeoJSONSerializer()
        