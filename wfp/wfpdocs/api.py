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

import json
import time
from urlparse import urlparse
import base64

from django.contrib.auth import authenticate
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.db.models import Count
from django.core.serializers.json import DjangoJSONEncoder

from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.authentication import BasicAuthentication
from tastypie.serializers import Serializer
from guardian.shortcuts import get_anonymous_user
from guardian.shortcuts import get_objects_for_user
from taggit.models import Tag

from geonode.base.models import ResourceBase, Region
from geonode.api.api import TagResource, TypeFilteredResource
from geonode.api.authorization import GeoNodeAuthorization

from models import WFPDocument, Category


class MixedBasicAuthentication(BasicAuthentication):
    """
    Custom authentication that mix BasicAuthentication (needed from OPWeb) and Authentication.
    Unluckily it seems that MultiAuthentication does not help when mixing those two ones,
    see: https://github.com/django-tastypie/django-tastypie/issues/1390
    """

    def is_authenticated(self, request, **kwargs):
        """
        Checks a user's basic auth credentials against the current
        Django auth backend.
        Otherwise just return True, as the static maps API is read only.
        """
        if not request.META.get('HTTP_AUTHORIZATION'):
            return True

        try:
            (auth_type, data) = request.META['HTTP_AUTHORIZATION'].split()
            if auth_type.lower() != 'basic':
                return self._unauthorized()
            user_pass = base64.b64decode(data).decode('utf-8')
        except:
            return self._unauthorized()

        bits = user_pass.split(':', 1)

        if len(bits) != 2:
            return self._unauthorized()

        if self.backend:
            user = self.backend.authenticate(username=bits[0], password=bits[1])
        else:
            user = authenticate(username=bits[0], password=bits[1])

        if user is None:
            return self._unauthorized()

        if not self.check_active(user):
            return False

        request.user = user
        return True


class CommonMetaApi:
    allowed_methods = ['get']
    include_resource_uri = True
    authentication = MixedBasicAuthentication()
    authorization = GeoNodeAuthorization()


class CountJSONSerializerWFPDocs(Serializer):
    """Custom serializer to post process the api and add counts for static maps"""

    def get_resources_counts(self, options):
        if settings.SKIP_PERMS_FILTER:
            resources = ResourceBase.objects.all()
        else:
            resources = get_objects_for_user(
                options['user'],
                'base.view_resourcebase'
            )
        if settings.RESOURCE_PUBLISHING:
            resources = resources.filter(is_published=True)

        if options['title_filter']:
            resources = resources.filter(title__icontains=options['title_filter'])

        resources = resources.instance_of(WFPDocument)

        counts = list(resources.values(options['count_type']).annotate(count=Count(options['count_type'])))

        return dict([(c[options['count_type']], c['count']) for c in counts])

    def to_json(self, data, options=None):
        options = options or {}
        data = self.to_simple(data, options)
        counts = self.get_resources_counts(options)
        if 'objects' in data:
            for item in data['objects']:
                item['count'] = counts.get(item['id'], 0)
        # Add in the current time.
        data['requested_time'] = time.time()

        return json.dumps(data, cls=DjangoJSONEncoder, sort_keys=True)


class RegionResource(TypeFilteredResource):
    """ Resource for Region filtered for WFPDocument """

    def serialize(self, request, data, format, options={}):
        options['count_type'] = 'regions'
        options['user'] = request.user

        return super(RegionResource, self).serialize(request, data, format, options)

    class Meta:
        queryset = Region.objects.all().order_by('name')
        resource_name = 'wfp-regions'
        allowed_methods = ['get']
        filtering = {
            'name': ALL,
            'code': ALL,
        }
        if settings.API_INCLUDE_REGIONS_COUNT:
            serializer = CountJSONSerializerWFPDocs()


class TagResourceSimple(ModelResource):
    """ Resource for Tag filtered for WFPDocument"""

    count = fields.IntegerField()

    class Meta(CommonMetaApi):
        resource_name = 'wfp-keywords'
        ctype = ContentType.objects.get_for_model(WFPDocument)
        queryset = Tag.objects.filter(taggit_taggeditem_items__content_type=ctype).distinct().order_by('name')

    def dehydrate_count(self, bundle):
        tags = bundle.obj.taggit_taggeditem_items
        ctype = ContentType.objects.get_for_model(WFPDocument)
        count = tags.filter(
                content_type=ctype).count()
        return count


class CategoryResource(ModelResource):
    """Resource  for Category"""

    count = fields.IntegerField()

    def dehydrate_count(self, bundle):
        return bundle.obj.wfpdocument_set.count()

    class Meta(CommonMetaApi):
        queryset = Category.objects.all()
        resource_name = 'wfp-categories'
        excludes = ['id', ]
        filtering = {
            'name': ALL,
        }


class WFPDocumentResource(ModelResource):
    """Resource for Static Map"""

    keywords = fields.ToManyField(TagResource, 'keywords', null=True)
    categories = fields.ToManyField(CategoryResource, 'categories', full=True)
    regions = fields.ToManyField(RegionResource, 'regions', full=True)
    file_size = fields.CharField(attribute='get_file_size', readonly=True)
    geonode_page = fields.CharField(attribute='detail_url', readonly=True)
    geonode_file = fields.FileField(attribute='doc_file')
    thumbnail = fields.CharField(attribute='thumbnail', readonly=True, null=True)
    is_public = fields.BooleanField(default=True)

    class Meta(CommonMetaApi):
        queryset = WFPDocument.objects.all().order_by('-date')
        resource_name = 'staticmaps'
        filtering = {
            'title': ALL,
            'keywords': ALL_WITH_RELATIONS,
            'categories': ALL_WITH_RELATIONS,
            'regions': ALL_WITH_RELATIONS,
            'date': ALL,
        }
        excludes = [
            'abstract',
            'bbox_x0', 'bbox_x1', 'bbox_y0', 'bbox_y1',
            'constraints_other',
            'csw_anytext',
            'csw_insert_date',
            'csw_mdsource',
            'csw_schema',
            'csw_type',
            'csw_typename',
            'csw_wkt_geometry',
            'data_quality_statement',
            'date_type',
            'distribution_description',
            'distribution_url',
            'edition',
            'extension',
            'featured',
            'is_published',
            'language',
            'maintenance_frequency',
            'metadata_uploaded',
            'metadata_xml',
            'owner',
            'share_count',
            'srid',
            'supplemental_information',
            'temporal_extent_end',
            'temporal_extent_start',
            # renamed
            'doc_file',
        ]

    def dehydrate_is_public(self, bundle):
        anonymous_user = get_anonymous_user()
        public_wfpdocs_ids = get_objects_for_user(
            anonymous_user, 'base.view_resourcebase'
            ).instance_of(WFPDocument).values_list('id', flat=True)
        return bundle.obj.id in public_wfpdocs_ids

    def dehydrate_page_format(self, bundle):
        return WFPDocument.FORMAT_CHOICES[bundle.data['page_format']][1]

    def dehydrate_orientation(self, bundle):
        return WFPDocument.ORIENTATION_CHOICES[bundle.data['orientation']][1]

    def dehydrate_thumbnail(self, bundle):
        url = urlparse(bundle.obj.thumbnail_url)
        return url.path

    def build_schema(self):
        base_schema = super(WFPDocumentResource, self).build_schema()
        for f in self._meta.object_class._meta.fields:
            if f.name in base_schema['fields'] and f.choices:
                base_schema['fields'][f.name].update({
                    'choices': f.choices,
                })
        return base_schema
