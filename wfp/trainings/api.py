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

from django.contrib.contenttypes.models import ContentType

from tastypie.resources import ModelResource
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie import fields
from taggit.models import Tag

from geonode.api.resourcebase_api import LayerResource
from geonode.api.api import TagResource

from .models import Training


class TagResourceSimple(TagResource):
    """ Tag API for models not inhereting form ResourceBase """

    class Meta:
        resource_name = 'keywords'
        ctype = ContentType.objects.get_for_model(Training)
        queryset = Tag.objects.filter(taggit_taggeditem_items__content_type=ctype).distinct().order_by('name')
        filtering = {
            'slug': ALL,
        }

    def dehydrate_count(self, bundle):
        tags = bundle.obj.taggit_taggeditem_items
        ctype = ContentType.objects.get_for_model(Training)
        count = tags.filter(
                content_type=ctype).count()
        return count


class TrainingResource(ModelResource):

    """ Training API """

    keywords = fields.ToManyField(TagResourceSimple, 'keywords', null=True, full=True)
    layers = fields.ToManyField(LayerResource, 'layers', null=True, full=True)

    def build_filters(self, filters={}):
        orm_filters = super(TrainingResource, self).build_filters(filters)
        keywords = filters.getlist("keywords__slug__in")

        if keywords:
            orm_filters.update({'keywords__slug__in': keywords})
        print orm_filters
        return orm_filters

    def apply_filters(self, request, applicable_filters):
        keywords = applicable_filters.pop('keywords__slug__in', None)
        trainings = super(TrainingResource, self).apply_filters(request, applicable_filters)
        if keywords:
            trainings = trainings.filter(keywords__slug__in=keywords).distinct()
        return trainings

    class Meta:
        queryset = Training.objects.all().order_by('title')
        resource_name = 'trainings'
        allowed_methods = ['get']
        filtering = {
            'slug': ALL,
            'keywords': ALL_WITH_RELATIONS,
            'layers': ALL_WITH_RELATIONS,
        }
        include_absolute_url = True
