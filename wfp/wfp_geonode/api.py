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

from django.contrib.auth import get_user_model
from django.conf import settings

from tastypie import fields
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.resources import ModelResource
from guardian.shortcuts import get_objects_for_user

from geonode.api.authorization import GeoNodeAuthorization
from geonode.api.api import ProfileResource
from geonode.api.api import CountJSONSerializer
from geonode.base.models import ResourceBase

from wfp.wfpdocs.models import WFPDocument


class WfpProfileResource(ProfileResource):
    """ WFP Profile API """

    wfpdocs_count = fields.IntegerField(default=0)

    def dehydrate_wfpdocs_count(self, bundle):
        obj_with_perms = get_objects_for_user(bundle.request.user,
                                              'base.view_resourcebase').instance_of(WFPDocument)
        return bundle.obj.resourcebase_set.filter(id__in=obj_with_perms.values('id')).distinct().count()

    class Meta:
        queryset = get_user_model().objects.exclude(username='AnonymousUser')
        resource_name = 'wfp-profiles'
        authorization = GeoNodeAuthorization()
        allowed_methods = ['get']
        ordering = ['username', 'date_joined']
        excludes = ['is_staff', 'password', 'is_superuser',
                    'is_active', 'last_login']

        filtering = {
            'username': ALL,
        }
        serializer = CountJSONSerializer()


class FeaturedMapResource(ModelResource):
    """ WFP Featured Maps API """

    owner = fields.ToOneField(ProfileResource, 'owner', full=True)
    custom_thumbnail = fields.FileField()

    def dehydrate_custom_thumbnail(self, bundle):
        from wfp.gis.models import CustomThumbnail
        rb = bundle.obj
        thumb = CustomThumbnail.objects.filter(object_id=rb.id, content_type=rb.polymorphic_ctype).first()
        # we cascade to default thumbnail if custom does not exist
        thumb_url = rb.thumbnail_url
        if thumb:
            thumb_url = '%s%s' % (settings.MEDIA_URL, thumb.thumbnail)
        return thumb_url

    class Meta:
        queryset = ResourceBase.objects.filter(featured=True).order_by('-date')
        if settings.RESOURCE_PUBLISHING:
            queryset = queryset.filter(is_published=True)
        resource_name = 'wfp-featured-maps'
        authorization = GeoNodeAuthorization()
        allowed_methods = ['get']
        filtering = {'title': ALL,
                     'keywords': ALL_WITH_RELATIONS,
                     'regions': ALL_WITH_RELATIONS,
                     'category': ALL_WITH_RELATIONS,
                     'owner': ALL_WITH_RELATIONS,
                     'date': ALL,
                     }
        ordering = ['date', 'title', 'popular_count']
        max_limit = None
