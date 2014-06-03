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
        include_resource_uri = False
        allowed_methods = ['get']
                 
class ProfileResource(GisModelResource):
    
    class Meta:
        queryset = Profile.objects.all()
        resource_name = 'profile'
        fields = ['name', 'position',]
        include_resource_uri = False
        allowed_methods = ['get']
        
class EmployeeResource(GisModelResource):
    
    profile = fields.ToOneField(ProfileResource, 'profile', full=True)
    office = fields.ToOneField(OfficeResource, 'office', full=True)
    
    class Meta:
        queryset = Employee.objects.all()
        resource_name = 'employee'
        filtering = {
            'profile': ALL_WITH_RELATIONS,
            'office': ALL_WITH_RELATIONS,
            'duties_type': ALL,
        }
        serializer = GeoJSONSerializer()
        include_resource_uri = False
        allowed_methods = ['get']
        
    def dehydrate_duties_type(self, bundle):
        duties_value = bundle.data['duties_type']
        if duties_value is not None:
            return Employee.DUTIES_CHOICES[bundle.data['duties_type']][1]
        else:
            return None
        
    def build_schema(self):
        base_schema = super(EmployeeResource, self).build_schema()
        for f in self._meta.object_class._meta.fields:
            if f.name in base_schema['fields'] and f.choices:
                base_schema['fields'][f.name].update({
                    'choices': f.choices,
                })
        return base_schema
    
        
