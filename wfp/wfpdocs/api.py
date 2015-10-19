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

from urlparse import urlparse

from django.contrib.contenttypes.models import ContentType

from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.authentication import BasicAuthentication, MultiAuthentication, Authentication
from guardian.shortcuts import get_anonymous_user
from guardian.shortcuts import get_objects_for_user
from taggit.models import Tag

from geonode.api.api import TagResource, RegionResource
from geonode.api.authorization import GeoNodeAuthorization

from models import WFPDocument, Category


class CommonMetaApi:
    allowed_methods = ['get']
    include_resource_uri = True
    authentication = MultiAuthentication(
            Authentication(),
            BasicAuthentication(),
    )
    authorization = GeoNodeAuthorization()


class TagResourceSimple(ModelResource):
    """ Resource for Tag not inhereting from ResourceBase"""

    class Meta(CommonMetaApi):
        resource_name = 'keywords'
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
        resource_name = 'wfpcategories'
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
            'thumbnail_url',
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
