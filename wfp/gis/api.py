#!/usr/bin/env python
#########################################################################
#
# Copyright (C) 2012-2015 Paolo Corti, pcorti@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################

from tastypie.contrib.gis.resources import ModelResource
from tastypie import fields
from tastypie.constants import ALL, ALL_WITH_RELATIONS

from geonode.people.models import Profile

from models import Office, Employee
from geojson import GeoJSONSerializer


class GisModelResource(ModelResource):
    """Abstract resource  for GIS application"""

    def serialize(self, request, data, format, options=None):
        """
        Override to parse the parameter and look for the geojson option.
        """
        options = options or {}
        options['geojson'] = request.GET and (
            request.GET.get('geojson', '0').lower() in ['', 'true', '1']
        )
        return super(ModelResource, self).serialize(request, data, format, options)


class OfficeResource(GisModelResource):
    """Resource  for Office"""

    class Meta:
        queryset = Office.objects.all()
        resource_name = 'office'
        fields = ['id', 'country', 'facility', 'place', 'source', 'status', 'wfpregion', 'geometry', ]
        filtering = {
            'place': ALL,
            'status': ALL,
            'wfpregion': ALL,
        }
        serializer = GeoJSONSerializer()
        include_resource_uri = False
        allowed_methods = ['get']


class ProfileResource(GisModelResource):
    """Resource  for Profile"""

    name = fields.CharField(readonly=True)

    class Meta:
        queryset = Profile.objects.all()
        resource_name = 'profile'
        fields = ['position', ]
        include_resource_uri = False
        allowed_methods = ['get']

    def dehydrate_name(self, bundle):
        return '%s %s' % (bundle.obj.first_name, bundle.obj.last_name)


class EmployeeResource(GisModelResource):
    """Resource  for Employee"""

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
